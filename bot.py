# ============================================================
# bot.py - Projeto de "chatbot" educativo em Discord
# ============================================================


import sys, os, discord
from utils.admin_checker import is_env_admin
from controller.user_commands import UserCommands
from dotenv import load_dotenv
from discord.ext import commands
from view.discord_view import DiscordView
from utils.logger import bot_logger

"""Carrega as variáveis de ambiente do arquivo .env"""
try:
    load_dotenv()
    bot_logger.info("Variáveis de ambiente carregadas com sucesso")
except Exception as e:
    bot_logger.critical(f"Erro ao carregar variáveis de ambiente: {str(e)}")
    sys.exit(1)


"""Configuração do bot """
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
view = DiscordView(bot)
controller = UserCommands(view)

""" Remover o comando help padrão e usar nosso próprio"""
bot.remove_command('help')


# === Eventos base do bot ===

@bot.event
async def on_ready():
    bot_logger.info(f'Bot {bot.user} está online!')
    bot_logger.info(f'ID do Bot: {bot.user.id}')
    bot_logger.info(f'Versão do Discord.py: {discord.__version__}')
    bot_logger.info(f'Latência: {round(bot.latency * 1000)}ms')
    bot_logger.info(f'Conectado em {len(bot.guilds)} servidores')
    print(f'{bot.user} está online!')

""" Tratamento personalizado de mensagens para intercetar comandos desconhecidos"""
@bot.event
async def on_message(message):
    # Ignora mensagens do próprio bot
    if message.author == bot.user:
        return
        
    # Verificar se é um comando (começa com !)
    if message.content.startswith('!'):
        command_name = message.content[1:].split()[0].lower()
        
        # Verificar se o comando existe
        if command_name not in [c.name for c in bot.commands]:
            # Enviar mensagem para comandos desconhecidos
            await message.channel.send(f"O comando `!{command_name}` não foi reconhecido. Digite `!ajuda` para ver os comandos disponíveis.")
            return
            
    # Processar o comando normalmente
    await bot.process_commands(message)

"""Tratamento de erros gerais"""
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):       
        pass
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Faltam argumentos para este comando. Use !help {ctx.command} para mais informações.")
    elif isinstance(error, commands.CheckFailure):
        await ctx.send("Você não tem permissão para usar este comando.")
    else:
        await ctx.send(f"Ocorreu um erro ao processar o comando: {error}")
        bot_logger.error(f"Erro ao processar comando: {error}")


# === Registo dinâmico de comandos ===


def register_command(name, func):
    @bot.command(name=name)
    async def cmd(ctx):
        try:
            await func(ctx)
        except Exception as e:
            bot_logger.error(f"Erro ao processar comando {name}: {str(e)}")
            await ctx.send(f"Erro ao processar o comando: {str(e)}")

for name, func in controller.get_commands().items():
    register_command(name, func)


# === Comando de verificação admin ===


@bot.command()
async def verificaradmin(ctx):
    """Verifica o status de administrador do usuário"""
    is_discord_admin = ctx.author.guild_permissions.administrator
    is_env_admin = view.admin_checker.is_admin(str(ctx.author.id))

    embed = discord.Embed(
        title="Status de Administrador",
        description=f"Verificação para {ctx.author.name}",
        color=discord.Color.blue()
    )

    embed.add_field(
        name="ID do Usuário",
        value=str(ctx.author.id),
        inline=False
    )

    embed.add_field(
        name="Admin por Permissão Discord",
        value="✅ Sim" if is_discord_admin else "❌ Não",
        inline=True
    )

    embed.add_field(
        name="Admin por Configuração (.env)",
        value="✅ Sim" if is_env_admin else "❌ Não",
        inline=True
    )

    await ctx.send(embed=embed)
    bot_logger.info(f"Verificação de admin realizada para {ctx.author.name} (ID: {ctx.author.id})")


# === Comandos administrativos ===


@bot.command()
@is_env_admin()
async def relatorio(ctx):
    """Gera um relatório completo de uso do bot"""
    try:
        await view.process_command(ctx, "relatorio")
    except Exception as e:
        bot_logger.error(f"Erro ao processar comando relatorio: {str(e)}")
        await ctx.send(f"Erro ao processar o comando: {str(e)}")

@bot.command()
@is_env_admin()
async def estatisticas(ctx):
    """Mostra estatísticas de uso do bot"""
    try:
        await view.process_command(ctx, "estatisticas")
    except Exception as e:
        bot_logger.error(f"Erro ao processar comando estatisticas: {str(e)}")
        await ctx.send(f"Erro ao processar o comando: {str(e)}")

@bot.command()
@is_env_admin()
async def historico(ctx, user: discord.Member):
    """Mostra o histórico de comandos de um usuário específico."""
    try:
        historico = view.consulta_model.obter_historico_utilizador(str(user.id))

        if not historico:
            await ctx.send(f"❌ Nenhum histórico encontrado para o usuário {user.name}.")
            return

        embed = discord.Embed(
            title=f"Histórico de Comandos de {user.name}",
            description=f"Total de consultas: **{len(historico)}**",
            color=discord.Color.green()
        )

        for consulta in historico[-10:]:  # Mostra os últimos 10 registros
            data = consulta["data"].split("T")[0] if "T" in consulta["data"] else consulta["data"].split(" ")[0]
            comando = consulta["comando"]
            secao = consulta["secao"] if consulta["secao"] else "Nenhuma seção"
            embed.add_field(
                name=f"{data} - {comando}",
                value=f"Seção: {secao}",
                inline=False
            )

        await ctx.send(embed=embed)
    except Exception as e:
        bot_logger.error(f"Erro ao processar comando historico: {str(e)}")
        await ctx.send(f"Erro ao processar o comando: {str(e)}")

@bot.command()
@is_env_admin()
async def grafico_comandos(ctx):
    """Gera um gráfico dos comandos mais utilizados"""
    try:
        await view.process_command(ctx, "grafico_comandos")
    except Exception as e:
        bot_logger.error(f"Erro ao processar comando grafico_comandos: {str(e)}")
        await ctx.send(f"Erro ao processar o comando: {str(e)}")

@bot.command()
@is_env_admin()
async def grafico_seccoes(ctx):
    """Gera um gráfico das seções mais consultadas"""
    try:
        await view.process_command(ctx, "grafico_seccoes")
    except Exception as e:
        bot_logger.error(f"Erro ao processar comando grafico_seccoes: {str(e)}")
        await ctx.send(f"Erro ao processar o comando: {str(e)}")


# === Comando de ajuda ===


@bot.command()
async def ajuda(ctx, command_name=None):
    """Comando alternativo de ajuda para evitar conflito com o help padrão"""
    try:
        if command_name:
            await view.process_command(ctx, "help", command_name)
        else:
            await view.process_command(ctx, "help")
    except Exception as e:
        bot_logger.error(f"Erro ao processar comando ajuda: {str(e)}")
        await ctx.send(f"Erro ao processar o comando: {str(e)}")

@bot.command()
async def help(ctx, command_name=None):
    """Comando de ajuda personalizado"""
    try:
        if command_name:
            await view.process_command(ctx, "help", command_name)
        else:
            await view.process_command(ctx, "help")
    except Exception as e:
        bot_logger.error(f"Erro ao processar comando help: {str(e)}")
        await ctx.send(f"Erro ao processar o comando: {str(e)}")


# === Execução do bot ===

try:
    bot_logger.info("Iniciando conexão com o Discord...")
    bot.run(os.getenv('DISCORD_TOKEN'))
except Exception as e:
    bot_logger.critical(f"Erro fatal ao iniciar o bot: {str(e)}")
    sys.exit(1)
