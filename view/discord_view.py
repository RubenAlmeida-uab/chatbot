import discord
from datetime import datetime
from pathlib import Path
from controller.bot_controller import BotController
from controller.user_controller import UserController
from utils.logger import bot_logger
from utils.admin_checker import AdminChecker
from model.consulta_model import ConsultaModel

class DiscordView:
    """
    Responsável pelo View.
    Apresentação de comandos e ficheiros para os utilizadores e administradores.
    """

    def __init__(self, bot):
        self.bot = bot
        self.controller = UserController()
        self.bot.controller = BotController()
        self.data_dir = Path("dados/puc")
        self.admin_checker = AdminChecker()
        self.consulta_model = ConsultaModel()

        # Registra listeners do bot controller
        self.bot.controller.adicionar_listener_estatisticas_acedidas(self._on_estatisticas_acedidas)
        self.bot.controller.adicionar_listener_relatorio_gerado(self._on_relatorio_gerado)
        self.bot.controller.adicionar_listener_grafico_gerado(self._on_grafico_gerado)
        self.bot.controller.adicionar_listener_erro(self._on_erro)


        bot_logger.info("DiscordView inicializada com sucesso")
    async def process_command(self, ctx, command_name: str, *args) -> None:
        """
        Processa um comando recebido do Discord e envia para o controller apropriado.

        Args:
            ctx: Contexto do comando do Discord
            command_name: Nome do comando
            args: Argumentos adicionais do comando
        """
        try:
            bot_logger.info(f"Comando recebido: {command_name} de {ctx.author.name} (ID: {ctx.author.id})")

            if command_name in self.controller.comandos_validos:
                await self._handle_puc_command(ctx, command_name)
            elif command_name in ["relatorio", "estatisticas", "historico", "grafico_comandos", "grafico_seccoes"]:
                await self._handle_admin_command(ctx, command_name, *args)
            elif command_name == "help":
                await self._handle_help_command(ctx, *args)
            else:
                bot_logger.warning(f"Comando não reconhecido: {command_name}")
                await ctx.send(f"Comando '{command_name}' não reconhecido. Use !help para ver os comandos disponíveis.")

        except Exception as e:
            bot_logger.error(f"Erro ao processar comando {command_name}: {str(e)}")
            await ctx.send(f"Erro ao processar o comando: {str(e)}")

    async def _handle_puc_command(self, ctx, command_name: str) -> None:
        """Processa comandos relacionados à PUC."""
        dados = self.controller.processar_comando(ctx.author.id, ctx.author.name, command_name)
        resposta = self._formatar_resposta(command_name, dados)
        await self._send_formatted_response(ctx, command_name, resposta)
        bot_logger.debug(f"Comando {command_name} processado com sucesso")

        self.consulta_model.registar_consulta(
            str(ctx.author.id),
            ctx.author.name,
            command_name,
            command_name
        )

    async def _handle_admin_command(self, ctx, command_name: str, *args) -> None:
        """Processa comandos administrativos."""
        if not await self._check_admin_permission(ctx):
            bot_logger.warning(
                f"Tentativa de acesso não autorizado ao comando admin {command_name} por {ctx.author.name}")
            await ctx.send("Este comando é restrito a administradores.")
            return

        bot_logger.info(f"Processando comando administrativo {command_name}")

        try:
            if command_name == "relatorio":
                report_file = await self.bot.controller.gerar_relatorio(str(ctx.author.id))
                await ctx.send("Aqui está o relatório solicitado:", file=report_file)
            elif command_name == "estatisticas":
                estatisticas = self.bot.controller.obter_estatisticas(str(ctx.author.id))
                await self._send_statistics_response(ctx, estatisticas)
            elif command_name == "historico":
                await self._handle_historico_command(ctx, *args)
            elif command_name in ["grafico_comandos", "grafico_seccoes"]:
                await self._handle_graph_command(ctx, command_name)

            bot_logger.debug(f"Comando administrativo {command_name} processado com sucesso")

        except Exception as e:
            bot_logger.error(f"Erro ao processar comando administrativo {command_name}: {str(e)}")
            await ctx.send(f"Erro ao processar o comando: {str(e)}")

    async def _handle_historico_command(self, ctx, *args) -> None:
        """Processa o comando de histórico."""
        if not args:
            await ctx.send("Por favor, mencione um utilizador para ver seu histórico.")
            return
        historico = self.bot.controller.obter_utilizador_historico(args[0], str(ctx.author.id))
        await self._send_user_history_response(ctx, historico)

    async def _handle_graph_command(self, ctx, command_name: str) -> None:
        """Processa comandos de gráficos."""
        if command_name == "grafico_comandos":
            graph_file = await self.bot.controller.gerar_grafico_comandos(str(ctx.author.id))
            await ctx.send("Aqui está o gráfico de comandos:", file=graph_file)
        elif command_name == "grafico_seccoes":
            graph_file = await self.bot.controller.gerar_grafico_seccoes(str(ctx.author.id))
            await ctx.send("Aqui está o gráfico de seções:", file=graph_file)

    async def _handle_help_command(self, ctx, *args) -> None:
        """Processa o comando de ajuda."""
        if len(args) > 0:
            await self._send_command_help(ctx, args[0])
            bot_logger.debug(f"Help específico enviado para comando {args[0]}")
        else:
            await self._send_command_list(ctx)
            bot_logger.debug("Lista completa de comandos enviada")

    async def _send_statistics_response(self, ctx, stats: dict) -> None:
        """Envia uma resposta formatada com estatísticas."""
        try:
            formatted_stats = self._formatar_estatisticas_para_discord(stats)
            await self._send_formatted_response(ctx, "estatisticas", formatted_stats)
            bot_logger.debug("Estatísticas enviadas com sucesso")

        except Exception as e:
            bot_logger.error(f"Erro ao enviar estatísticas: {str(e)}")
            raise

    def _formatar_data(self, data_str):
        """Formata uma string de data ISO para um formato legível."""
        if not data_str:
            return ""
        try:
            data_obj = datetime.fromisoformat(data_str)
            return data_obj.strftime('%d/%m/%Y %H:%M:%S')
        except (ValueError, TypeError):
            return data_str

    def _formatar_estatisticas_para_discord(self, estatisticas):
        """Formata as estatísticas para apresentação na interface Discord."""
        primeiro_acesso = self._formatar_data(estatisticas.get('primeiro_acesso', ''))
        ultimo_acesso = self._formatar_data(estatisticas.get('ultimo_acesso', ''))
        return {
            "titulo": "Estatísticas do Bot",
            "descricao": "Resumo de uso do bot",
            "seccoes": [
                {
                    "titulo": "Informações Gerais",
                    "itens": [
                        f"Total de consultas: {estatisticas['total_consultas']}",
                        f"Utilizadores únicos: {estatisticas['utilizadores_unicos']}",
                        f"Primeiro acesso: {primeiro_acesso}",
                        f"Último acesso: {ultimo_acesso}"
                    ]
                },
                {
                    "titulo": "Top 5 Comandos",
                    "itens": [f"{cmd}: {count} vezes" for cmd, count in estatisticas['comandos_populares'][:5]] or ["Nenhum comando registrado"]
                },
                {
                    "titulo": "Top 5 Seções",
                    "itens": [f"{secao}: {count} vezes" for secao, count in estatisticas['seccoes_populares'][:5]] or ["Nenhuma seção registrada"]
                },
                {
                    "titulo": "Top 5 Utilizadores",
                    "itens": [f"{nome} (ID: {uid}): {count} consultas" for uid, nome, count in estatisticas['utilizadores_ativos'][:5]] or ["Nenhum utilizador registrado"]
                }
            ]
        }

    def _read_puc_file(self, filename: str) -> str:
        """Lê o conteúdo de um ficheiro da pasta dados/puc."""
        file_path = self.data_dir / f"{filename}.txt"
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                bot_logger.debug(f"Arquivo {filename}.txt lido com sucesso")
                return content
        except FileNotFoundError:
            bot_logger.error(f"Arquivo {filename}.txt não encontrado")
            return f"Ficheiro {filename} não encontrado."

    async def _send_formatted_response(self, ctx, command_name: str, content) -> None:
        """Envia uma resposta formatada para o Discord."""
        try:
            # Se for dict (como no caso das estatísticas), cria embed personalizado
            if isinstance(content, dict) and "seccoes" in content:
                embed = discord.Embed(
                    title=content.get("titulo", "Informação"),
                    description=content.get("descricao", ""),
                    color=discord.Color.blue()
                )

                for sec in content["seccoes"]:
                    titulo = sec.get("titulo", "")
                    itens = "\n".join(sec.get("itens", []))
                    embed.add_field(name=titulo, value=itens, inline=False)

                await ctx.send(embed=embed)
                bot_logger.debug(f"Resposta de estatísticas enviada para comando {command_name}")
                return

            # Caso contrário, assume conteúdo textual
            if not isinstance(content, str):
                content = str(content)

            lines = content.split('\n')
            title = lines[0].replace('#', '').strip()
            description = '\n'.join(lines[1:]).strip()

            embed = discord.Embed(
                title=title,
                description=description,
                color=discord.Color.blue()
            )
            await ctx.send(embed=embed)
            bot_logger.debug(f"Resposta formatada enviada para comando {command_name}")

        except Exception as e:
            bot_logger.error(f"Erro ao enviar resposta formatada: {str(e)}")
            raise

    async def _check_admin_permission(self, ctx) -> bool:
        """Verifica se o utilizador tem permissões de administrador."""
        is_discord_admin = ctx.author.guild_permissions.administrator
        is_env_admin = self.admin_checker.is_admin(str(ctx.author.id))

        if is_env_admin:
            bot_logger.info(f"utilizador {ctx.author.name} (ID: {ctx.author.id}) autenticado como admin via .env")
        elif is_discord_admin:
            bot_logger.info(f"utilizador {ctx.author.name} (ID: {ctx.author.id}) autenticado como admin via Discord")
        else:
            bot_logger.warning(f"utilizador {ctx.author.name} (ID: {ctx.author.id}) não tem permissões de administrador")

        return is_discord_admin or is_env_admin

    async def _send_command_help(self, ctx, command_name: str) -> None:
        """Envia ajuda sobre um comando específico."""
        embed = discord.Embed(
            title=f"Ajuda: {command_name}",
            color=discord.Color.blue()
        )

        DESCRICAO_FIELD_NAME = "Descrição"

        if command_name in ["uc", "competencias", "roteiro", "metodologia", "recursos",
                            "calendario", "avaliacao", "exame", "ia", "estrutura", "cartao"]:
            embed.description = f"Mostra informações sobre {command_name} da unidade curricular"
            embed.add_field(name="Uso", value=f"!{command_name}", inline=False)

        elif command_name in ["relatorio", "estatisticas", "historico", "grafico_comandos", "grafico_seccoes"]:
            embed.description = "Comando administrativo"
            if command_name == "historico":
                embed.add_field(name="Uso", value="!historico @utilizador", inline=False)
            else:
                embed.add_field(name="Uso", value=f"!{command_name}", inline=False)
            embed.add_field(name="Permissão", value="Apenas administradores", inline=False)

            # Descrições específicas para cada comando admin
            if command_name == "relatorio":
                embed.add_field(name=DESCRICAO_FIELD_NAME, value="Gera um relatório completo de uso do bot em formato Markdown",
                                inline=False)
            elif command_name == "estatisticas":
                embed.add_field(name=DESCRICAO_FIELD_NAME, value="Mostra um resumo das estatísticas de uso do bot", inline=False)
            elif command_name == "historico":
                embed.add_field(name=DESCRICAO_FIELD_NAME, value="Mostra o histórico de comandos de um utilizador específico",
                                inline=False)
            elif command_name == "grafico_comandos":
                embed.add_field(name=DESCRICAO_FIELD_NAME, value="Gera um gráfico dos comandos mais utilizados", inline=False)
            elif command_name == "grafico_seccoes":
                embed.add_field(name=DESCRICAO_FIELD_NAME, value="Gera um gráfico das seções mais consultadas", inline=False)

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
                    "!relatorio - Gera relatório completo de uso",
                    "!estatisticas - Mostra estatísticas de uso",
                    "!historico @user - Histórico de um utilizador",
                    "!grafico_comandos - Gráfico dos comandos mais usados",
                    "!grafico_seccoes - Gráfico das seções mais consultadas"
                ]),
                inline=False
            )

        # Comandos de ajuda
        embed.add_field(
            name="Comandos de Ajuda",
            value="\n".join([
                "!help - Mostra esta lista de comandos",
                "!help <comando> - Mostra ajuda detalhada sobre um comando",
                "!ajuda - Alternativa ao comando help"
            ]),
            inline=False
        )

        await ctx.send(embed=embed)

    # === Event Handlers do Controller ===

    def _on_estatisticas_acedidas(self, admin_id: str, estatisticas: dict) -> None:
        """Handler para evento de estatísticas acessadas."""
        bot_logger.info(f"Estatísticas acessadas por admin {admin_id}")

    def _on_relatorio_gerado(self, admin_id: str, tipo_relatorio: str, caminho_ficheiro: str) -> None:
        """Handler para evento de relatório gerado."""
        bot_logger.info(f"Relatório {tipo_relatorio} gerado por admin {admin_id}: {caminho_ficheiro}")

    def _on_grafico_gerado(self, admin_id: str, tipo_grafico: str, caminho_ficheiro: str) -> None:
        """Handler para evento de gráfico gerado."""
        bot_logger.info(f"Gráfico {tipo_grafico} gerado por admin {admin_id}: {caminho_ficheiro}")

    def _on_erro(self, admin_id: str, operacao: str, mensagem_erro: str) -> None:
        """Handler para evento de erro."""
        bot_logger.error(f"Erro na operação {operacao} por admin {admin_id}: {mensagem_erro}")


    def _formatar_resposta(self, seccao, dados):
        """Formata a resposta com base na secção e nos dados obtidos."""
        resposta = f"**{seccao.upper()}**\n\n"
        if isinstance(dados, str):
            resposta += dados
        elif isinstance(dados, list):
            for i, item in enumerate(dados, 1):
                resposta += f"{i}. {item}\n"
        elif isinstance(dados, dict):
            for chave, valor in dados.items():
                resposta += f"**{chave}**: {valor}\n\n"
        return resposta