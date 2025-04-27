import discord
from pathlib import Path
from controller.bot_controller import BotController
from utils.logger import bot_logger
from utils.admin_checker import AdminChecker
from model.consulta_model import ConsultaModel



class DiscordView:
    """
    Classe responsável pela camada de View do chatbot no Discord.
    Gerencia a apresentação de comandos e ficheiros para os utilizadores e administradores.
    """

    def __init__(self, bot):
        self.bot = bot
        self.controller = BotController()
        self.data_dir = Path("dados/puc")
        self.admin_checker = AdminChecker()
        self.consulta_model = ConsultaModel()  # <-- ESTA LINHA É ESSENCIAL!!

        # Registra listeners do controller
        self.controller.adicionar_listener_estatisticas_acedidas(self._on_estatisticas_acedidas)
        self.controller.adicionar_listener_relatorio_gerado(self._on_relatorio_gerado)
        self.controller.adicionar_listener_grafico_gerado(self._on_grafico_gerado)
        self.controller.adicionar_listener_erro(self._on_erro)

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

            # Comandos relacionados à PUC (informações da disciplina)
            if command_name in ["uc", "competencias", "roteiro", "metodologia", "recursos",
                                "calendario", "avaliacao", "exame", "ia", "estrutura", "cartao"]:
                content = self._read_puc_file(command_name)
                await self._send_formatted_response(ctx, command_name, content)
                bot_logger.debug(f"Comando PUC {command_name} processado com sucesso")

                # ⚡ AQUI: registar a consulta!
                self.consulta_model.registar_consulta(
                    str(ctx.author.id),
                    ctx.author.name,
                    command_name,
                    command_name  # ou None se não quiseres associar seção
                )

            # Comandos administrativos
            elif command_name in ["relatorio", "estatisticas", "historico", "grafico_comandos", "grafico_seccoes"]:
                if not await self._check_admin_permission(ctx):
                    bot_logger.warning(
                        f"Tentativa de acesso não autorizado ao comando admin {command_name} por {ctx.author.name}")
                    await ctx.send("Este comando é restrito a administradores.")
                    return

                bot_logger.info(f"Processando comando administrativo {command_name}")

                try:
                    if command_name == "relatorio":
                        # Gera o relatório diretamente através do controller
                        report_file = await self.controller.gerar_relatorio(str(ctx.author.id))
                        await ctx.send("Aqui está o relatório solicitado:", file=report_file)
                    elif command_name == "estatisticas":
                        estatisticas = self.controller.obter_estatisticas(str(ctx.author.id))
                        await self._send_statistics_response(ctx, estatisticas)
                    elif command_name == "historico":
                        if not args:
                            await ctx.send("Por favor, mencione um usuário para ver seu histórico.")
                            return
                        historico = self.controller.obter_utilizador_historico(args[0], str(ctx.author.id))
                        await self._send_user_history_response(ctx, historico)
                    elif command_name == "grafico_comandos":
                        graph_file = await self.controller.gerar_grafico_comandos(str(ctx.author.id))
                        await ctx.send("Aqui está o gráfico de comandos:", file=graph_file)
                    elif command_name == "grafico_seccoes":
                        graph_file = await self.controller.gerar_grafico_seccoes(str(ctx.author.id))
                        await ctx.send("Aqui está o gráfico de seções:", file=graph_file)

                    bot_logger.debug(f"Comando administrativo {command_name} processado com sucesso")

                except Exception as e:
                    bot_logger.error(f"Erro ao processar comando administrativo {command_name}: {str(e)}")
                    await ctx.send(f"Erro ao processar o comando: {str(e)}")

            # Comando de ajuda
            elif command_name == "help":
                if len(args) > 0:
                    await self._send_command_help(ctx, args[0])
                    bot_logger.debug(f"Help específico enviado para comando {args[0]}")
                else:
                    await self._send_command_list(ctx)
                    bot_logger.debug("Lista completa de comandos enviada")

            else:
                bot_logger.warning(f"Comando não reconhecido: {command_name}")
                await ctx.send(f"Comando '{command_name}' não reconhecido. Use !help para ver os comandos disponíveis.")

        except Exception as e:
            bot_logger.error(f"Erro ao processar comando {command_name}: {str(e)}")
            await ctx.send(f"Erro ao processar o comando: {str(e)}")

    async def _send_statistics_response(self, ctx, stats: dict) -> None:
        """Envia uma resposta formatada com estatísticas."""
        try:
            embed = discord.Embed(
                title="Estatísticas do Bot",
                description="Resumo de uso do bot",
                color=discord.Color.blue()
            )

            # Informações gerais
            embed.add_field(
                name="Informações Gerais",
                value=f"Total de consultas: {stats['total_consultas']}\n"
                      f"Utilizadores únicos: {stats['utilizadores_unicos']}\n"
                      f"Primeiro acesso: {stats['primeiro_acesso']}\n"
                      f"Último acesso: {stats['ultimo_acesso']}",
                inline=False
            )

            # Comandos populares
            comandos_str = "\n".join(f"{cmd}: {count} vezes" for cmd, count in stats['comandos_populares'][:5])
            embed.add_field(
                name="Top 5 Comandos",
                value=comandos_str if comandos_str else "Nenhum comando registrado",
                inline=True
            )

            # Seções populares
            seccoes_str = "\n".join(f"{sec}: {count} vezes" for sec, count in stats['seccoes_populares'][:5])
            embed.add_field(
                name="Top 5 Seções",
                value=seccoes_str if seccoes_str else "Nenhuma seção registrada",
                inline=True
            )

            # Usuários mais ativos
            usuarios_str = "\n".join(f"{nome}: {count} comandos" for _, nome, count in stats['utilizadores_ativos'][:5])
            embed.add_field(
                name="Top 5 Usuários",
                value=usuarios_str if usuarios_str else "Nenhum usuário registrado",
                inline=False
            )

            await ctx.send(embed=embed)
            bot_logger.debug("Estatísticas enviadas com sucesso")

        except Exception as e:
            bot_logger.error(f"Erro ao enviar estatísticas: {str(e)}")
            raise

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

    async def _send_formatted_response(self, ctx, command_name: str, content: str) -> None:
        """Envia uma resposta formatada para o Discord."""
        try:
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
        """Verifica se o usuário tem permissões de administrador."""
        is_discord_admin = ctx.author.guild_permissions.administrator
        is_env_admin = self.admin_checker.is_admin(str(ctx.author.id))

        if is_env_admin:
            bot_logger.info(f"Usuário {ctx.author.name} (ID: {ctx.author.id}) autenticado como admin via .env")
        elif is_discord_admin:
            bot_logger.info(f"Usuário {ctx.author.name} (ID: {ctx.author.id}) autenticado como admin via Discord")
        else:
            bot_logger.warning(f"Usuário {ctx.author.name} (ID: {ctx.author.id}) não tem permissões de administrador")

        return is_discord_admin or is_env_admin

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

        elif command_name in ["relatorio", "estatisticas", "historico", "grafico_comandos", "grafico_seccoes"]:
            embed.description = "Comando administrativo"
            if command_name == "historico":
                embed.add_field(name="Uso", value="!historico @utilizador", inline=False)
            else:
                embed.add_field(name="Uso", value=f"!{command_name}", inline=False)
            embed.add_field(name="Permissão", value="Apenas administradores", inline=False)

            # Descrições específicas para cada comando admin
            if command_name == "relatorio":
                embed.add_field(name="Descrição", value="Gera um relatório completo de uso do bot em formato Markdown",
                                inline=False)
            elif command_name == "estatisticas":
                embed.add_field(name="Descrição", value="Mostra um resumo das estatísticas de uso do bot", inline=False)
            elif command_name == "historico":
                embed.add_field(name="Descrição", value="Mostra o histórico de comandos de um usuário específico",
                                inline=False)
            elif command_name == "grafico_comandos":
                embed.add_field(name="Descrição", value="Gera um gráfico dos comandos mais utilizados", inline=False)
            elif command_name == "grafico_seccoes":
                embed.add_field(name="Descrição", value="Gera um gráfico das seções mais consultadas", inline=False)

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