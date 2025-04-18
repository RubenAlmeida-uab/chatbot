import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from view.discord_view import DiscordView

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração do bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
view = DiscordView(bot)

@bot.event
async def on_ready():
    print(f'{bot.user} está online!')

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
async def relatorio(ctx):
    await view.process_command(ctx, "relatorio")

@bot.command()
async def estatisticas(ctx):
    await view.process_command(ctx, "estatisticas")

@bot.command()
async def historico(ctx, user: discord.Member):
    await view.process_command(ctx, "historico", user.id)

@bot.command()
async def help(ctx, command_name=None):
    if command_name:
        await view.process_command(ctx, "help", command_name)
    else:
        await view.process_command(ctx, "help")

# Inicia o bot com o token do arquivo .env
bot.run(os.getenv('DISCORD_TOKEN'))