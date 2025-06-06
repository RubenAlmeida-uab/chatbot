# ============================================================
# user_commands.py - Controlador de Comandos PUC via Discord
# ============================================================
# Unidade Curricular:
# Laboratório de Desenvolvimento de _Software_
#
# Objetivo:
# Este módulo define a classe _`UserCommands_`, responsável por
# gerir os comandos relacionados com a unidade curricular (PUC).
#
# Funcionalidades:
# 🔹 Redirecionamento de comandos do Discord para a View
# 🔹 Suporte a comandos informativos _como !uc, !roteiro, etc.
# 🔹 Integração com a _`DiscordView_` para formatação e envio de respostas
#
# Notas:
# - A nomenclatura _`usar_` indica que o método é chamado em resposta
#   ao uso de um comando específico no Discord.
# - A lista de comandos disponíveis é registada dinamicamente via `get_commands`.
# ============================================================

from model.dados_model import DadosModel
from model.consulta_model import ConsultaModel
from utils.logger import bot_logger


class UserCommands:
    def __init__(self, view):
        self.view = view

    async def usar_uc(self, ctx):
        await self.view.processar_comando(ctx, "uc")

    async def usar_roteiro(self, ctx):
        await self.view.processar_comando(ctx, "roteiro")

    async def usar_avaliacao(self, ctx):
        await self.view.processar_comando(ctx, "avaliacao")

    async def usar_competencias(self, ctx):
        await self.view.processar_comando(ctx, "competencias")
    
    async def usar_metodologia(self, ctx):
        await self.view.processar_comando(ctx, "metodologia")
    
    async def usar_recursos(self, ctx):
        await self.view.processar_comando(ctx, "recursos")
    
    async def usar_calendario(self, ctx):
        await self.view.processar_comando(ctx, "calendario")
    
    async def usar_exame(self, ctx):
        await self.view.processar_comando(ctx, "exame")
    
    async def usar_ia(self, ctx):
        await self.view.processar_comando(ctx, "ia")
    
    async def usar_estrutura(self, ctx):
        await self.view.processar_comando(ctx, "estrutura")
    
    async def usar_cartao(self, ctx):
        await self.view.processar_comando(ctx, "cartao")

    def obter_comandos(self):
        return {
            "uc": self.usar_uc,
            "roteiro": self.usar_roteiro,
            "avaliacao": self.usar_avaliacao,
            "competencias": self.usar_competencias,
            "metodologia": self.usar_metodologia,
            "recursos": self.usar_recursos,
            "calendario": self.usar_calendario,
            "exame": self.usar_exame,
            "ia": self.usar_ia,
            "estrutura": self.usar_estrutura,
            "cartao": self.usar_cartao
        }
