import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from view.discord_view import DiscordView
from utils.logger import bot_logger
import sys

# Configuração inicial do logger
bot_logger.info("Iniciando configuração do bot...")

# Carrega as variáveis de ambiente do arquivo .env
try:
    load_dotenv()
    bot_logger.info("Variáveis de ambiente carregadas com sucesso")
except Exception as e:
    bot_logger.critical(f"Erro ao carregar variáveis de ambiente: {str(e)}")
    sys.exit(1)

# Configuração do bot
try:
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix='!', intents=intents)
    view = DiscordView(bot)
    bot_logger.info("Bot configurado com sucesso")
except Exception as e:
    bot_logger.critical(f"Erro na configuração do bot: {str(e)}")
    sys.exit(1)


@bot.event
async def on_ready():
    bot_logger.info(f'Bot {bot.user} está online!')
    bot_logger.info(f'ID do Bot: {bot.user.id}')
    bot_logger.info(f'Versão do Discord.py: {discord.__version__}')
    bot_logger.info(f'Latência: {round(bot.latency * 1000)}ms')
    bot_logger.info(f'Conectado em {len(bot.guilds)} servidores')
    print(f'{bot.user} está online!')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        bot_logger.warning(f"Comando não encontrado: {ctx.message.content}")
        await ctx.send("Comando não encontrado. Use !help para ver os comandos disponíveis.")
    elif isinstance(error, commands.MissingRequiredArgument):
        bot_logger.warning(f"Argumentos faltando no comando: {ctx.message.content}")
        await ctx.send("Argumentos faltando. Use !help <comando> para ver como usar este comando.")
    elif isinstance(error, commands.MemberNotFound):
        bot_logger.warning(f"Membro não encontrado: {ctx.message.content}")
        await ctx.send("Usuário não encontrado. Certifique-se de mencionar um usuário válido.")
    else:
        bot_logger.error(f"Erro ao processar comando: {str(error)}")
        await ctx.send(f"Ocorreu um erro ao processar o comando: {str(error)}")


# Comandos básicos
@bot.command()
async def uc(ctx):
    await view.process_command(ctx, "uc")


@bot.command()
async def competencias(ctx):
    await view.process_command(ctx, "competencias")


@bot.command()
async def roteiro(ctx):
    await view.process_command(ctx, "roteiro")


@bot.command()
async def metodologia(ctx):
    await view.process_command(ctx, "metodologia")


@bot.command()
async def recursos(ctx):
    await view.process_command(ctx, "recursos")


@bot.command()
async def calendario(ctx):
    await view.process_command(ctx, "calendario")


@bot.command()
async def avaliacao(ctx):
    await view.process_command(ctx, "avaliacao")


@bot.command()
async def exame(ctx):
    await view.process_command(ctx, "exame")


@bot.command()
async def ia(ctx):
    await view.process_command(ctx, "ia")


@bot.command()
async def estrutura(ctx):
    await view.process_command(ctx, "estrutura")


@bot.command()
async def cartao(ctx):
    await view.process_command(ctx, "cartao")


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
        value="✅ Sim" if is_discord_admin else " Não",
        inline=True
    )

    embed.add_field(
        name="Admin por Configuração (.env)",
        value=" Sim" if is_env_admin else "Não",
        inline=True
    )

    await ctx.send(embed=embed)
    bot_logger.info(f"Verificação de admin realizada para {ctx.author.name} (ID: {ctx.author.id})")


# Comandos administrativos
@bot.command()
@commands.has_permissions(administrator=True)
async def relatorio(ctx):
    """Gera um relatório completo de uso do bot"""
    await view.process_command(ctx, "relatorio")


@bot.command()
@commands.has_permissions(administrator=True)
async def estatisticas(ctx):
    """Mostra estatísticas de uso do bot"""
    await view.process_command(ctx, "estatisticas")


@bot.command()
@commands.has_permissions(administrator=True)
async def historico(ctx, user: discord.Member):
    """Mostra o histórico de comandos de um usuário específico"""
    await view.process_command(ctx, "historico", user.id)


@bot.command()
@commands.has_permissions(administrator=True)
async def grafico_comandos(ctx):
    """Gera um gráfico dos comandos mais utilizados"""
    await view.process_command(ctx, "grafico_comandos")


@bot.command()
@commands.has_permissions(administrator=True)
async def grafico_seccoes(ctx):
    """Gera um gráfico das seções mais consultadas"""
    await view.process_command(ctx, "grafico_seccoes")


# Comandos de ajuda
@bot.command()
async def ajuda(ctx, command_name=None):
    """Comando alternativo de ajuda para evitar conflito com o help padrão"""
    if command_name:
        await view.process_command(ctx, "help", command_name)
    else:
        await view.process_command(ctx, "help")


# Remover o comando help padrão e usar nosso próprio
bot.remove_command('help')


@bot.command()
async def help(ctx, command_name=None):
    """Comando de ajuda personalizado"""
    if command_name:
        await view.process_command(ctx, "help", command_name)
    else:
        await view.process_command(ctx, "help")


# Tratamento de erros para comandos administrativos
@relatorio.error
@estatisticas.error
@historico.error
@grafico_comandos.error
@grafico_seccoes.error
async def admin_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        bot_logger.warning(f"Tentativa de acesso não autorizado ao comando admin por {ctx.author.name}")
        await ctx.send("Você precisa ter permissões de administrador para usar este comando.")
    else:
        await on_command_error(ctx, error)


try:
    bot_logger.info("Iniciando conexão com o Discord...")
    bot.run(os.getenv('DISCORD_TOKEN'))
except Exception as e:
    bot_logger.critical(f"Erro fatal ao iniciar o bot: {str(e)}")
    sys.exit(1)