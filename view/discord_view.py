import discord
from typing import Dict, List, Optional
import json
import os
from datetime import datetime
from pathlib import Path
from controller.bot_controller import BotController


class DiscordView:
    """
    Classe responsável pela camada de View do chatbot no Discord.
    Gerencia a apresentação de comandos e ficheiros para os utilizadores e administradores.
    """

    def __init__(self, bot):
        self.bot = bot
        self.controller = BotController()  # Instância do controller
        self.data_dir = Path("dados/puc")

        # Registra esta view como listener para eventos do controller
        self.controller.adicionar_listener_estatisticas_acedidas(self._on_estatisticas_acedidas)
        self.controller.adicionar_listener_relatorio_gerado(self._on_relatorio_gerado)
        self.controller.adicionar_listener_grafico_gerado(self._on_grafico_gerado)
        self.controller.adicionar_listener_erro(self._on_erro)

    async def process_command(self, ctx, command_name: str, *args) -> None:
        """
        Processa um comando recebido do Discord e envia para o controller apropriado.

        Args:
            ctx: Contexto do comando do Discord
            command_name: Nome do comando
            args: Argumentos adicionais do comando
        """
        try:
            # Comandos relacionados à PUC (informações da disciplina)
            if command_name in ["uc", "competencias", "roteiro", "metodologia", "recursos",
                                "calendario", "avaliacao", "exame", "ia", "estrutura", "cartao"]:
                content = self._read_puc_file(command_name)
                await self._send_formatted_response(ctx, command_name, content)

            # Comandos administrativos
            elif command_name in ["relatorio", "estatisticas", "historico"]:
                if not await self._check_admin_permission(ctx):
                    await ctx.send("Este comando é restrito a administradores.")
                    return

                result = await self.controller.processar_comando_admin(
                    str(ctx.author.id),
                    ctx.author.name,
                    command_name,
                    *args
                )

                if isinstance(result, discord.File):
                    await ctx.send(file=result)
                elif isinstance(result, str):
                    await ctx.send(result)
                elif isinstance(result, dict):
                    await self._send_formatted_response(ctx, command_name, result)

            # Comando de ajuda
            elif command_name == "help":
                if len(args) > 0:
                    await self._send_command_help(ctx, args[0])
                else:
                    await self._send_command_list(ctx)

            else:
                await ctx.send(f"Comando '{command_name}' não reconhecido. Use !help para ver os comandos disponíveis.")

        except Exception as e:
            await ctx.send(f"Erro ao processar o comando: {str(e)}")

    def _read_puc_file(self, filename: str) -> str:
        """Lê o conteúdo de um ficheiro da pasta dados/puc."""
        file_path = self.data_dir / f"{filename}.txt"
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return f"Ficheiro {filename} não encontrado."

    async def _send_formatted_response(self, ctx, command_name: str, content: str) -> None:
        """Envia uma resposta formatada para o Discord."""
        lines = content.split('\n')
        title = lines[0].replace('#', '').strip()
        description = '\n'.join(lines[1:]).strip()

        embed = discord.Embed(
            title=title,
            description=description,
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

    async def _check_admin_permission(self, ctx) -> bool:
        """Verifica se o usuário tem permissões de administrador."""
        return ctx.author.guild_permissions.administrator

    async def _send_command_help(self, ctx, command_name: str) -> None:
        """Envia ajuda sobre um comando específico."""
        embed = discord.Embed(
            title=f"Ajuda: {command_name}",
            color=discord.Color.blue()
        )

        if command_name in ["uc", "competencias", "roteiro", "metodologia", "recursos",
                            "calendario", "avaliacao", "exame", "ia", "estrutura", "cartao"]:
            embed.description = f"Mostra informações sobre {command_name} da unidade curricular"
            embed.add_field(name="Uso", value=f"!{command_name}", inline=False)

        elif command_name in ["relatorio", "estatisticas", "historico"]:
            embed.description = "Comando administrativo"
            if command_name == "historico":
                embed.add_field(name="Uso", value="!historico @utilizador", inline=False)
            else:
                embed.add_field(name="Uso", value=f"!{command_name}", inline=False)
            embed.add_field(name="Permissão", value="Apenas administradores", inline=False)

        else:
            embed.description = "Comando não encontrado"

        await ctx.send(embed=embed)

    async def _send_command_list(self, ctx) -> None:
        """Envia a lista de comandos disponíveis."""
        is_admin = await self._check_admin_permission(ctx)

        embed = discord.Embed(
            title="Comandos Disponíveis",
            description="Lista de todos os comandos do bot",
            color=discord.Color.green()
        )

        # Comandos da PUC
        embed.add_field(
            name="Comandos da Unidade Curricular",
            value="\n".join([
                "!uc - Informações gerais",
                "!competencias - Competências a desenvolver",
                "!roteiro - Conteúdo programático",
                "!metodologia - Metodologia de ensino",
                "!recursos - Recursos disponíveis",
                "!calendario - Datas importantes",
                "!avaliacao - Método de avaliação",
                "!exame - Informações sobre exames",
                "!ia - Uso de IA na UC",
                "!estrutura - Estrutura da equipa",
                "!cartao - Cartão de aprendizagem"
            ]),
            inline=False
        )

        # Comandos administrativos (apenas mostrados para admins)
        if is_admin:
            embed.add_field(
                name="Comandos Administrativos",
                value="\n".join([
                    "!relatorio - Gera relatório de uso",
                    "!estatisticas - Mostra estatísticas",
                    "!historico @user - Histórico de um utilizador"
                ]),
                inline=False
            )

        await ctx.send(embed=embed)

    # === Event Handlers do Controller ===

    def _on_estatisticas_acedidas(self, admin_id: str, estatisticas: dict) -> None:
        """Handler para evento de estatísticas acessadas."""
        pass  # Implementar se necessário

    def _on_relatorio_gerado(self, admin_id: str, tipo_relatorio: str, caminho_ficheiro: str) -> None:
        """Handler para evento de relatório gerado."""
        pass  # Implementar se necessário

    def _on_grafico_gerado(self, admin_id: str, tipo_grafico: str, caminho_ficheiro: str) -> None:
        """Handler para evento de gráfico gerado."""
        pass  # Implementar se necessário

    def _on_erro(self, admin_id: str, operacao: str, mensagem_erro: str) -> None:
        """Handler para evento de erro."""
        pass  # Implementar se necessário