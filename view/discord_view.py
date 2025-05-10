# ============================================================
# discord_view.py - _Interface e Gestão de Comandos no Discord
# ============================================================
# Unidade Curricular:
# Laboratório de Desenvolvimento de _Software_
#
# Objetivo:
# Este módulo define a view principal para interação com o utilizador:
# 🔹 Processamento de comandos de utilizadores e administradores
# 🔹 Verificação de permissões administrativas (via Discord e .env)
# 🔹 Geração e formatação de respostas via embeds no Discord
# 🔹 Gestão de eventos de estatísticas, relatórios e gráficos
#
# Notas:
# - _Integra com o BotController para lógica de negócio
# - Suporta ajuda contextual, histórico de comandos e visualização de dados
# ============================================================

import discord
from datetime import datetime
from pathlib import Path
from controller.bot_controller import BotController
from controller.user_controller import UserController
from utils.logger import bot_logger
from utils.admin_checker import AdminChecker
from model.consulta_model import ConsultaModel


# noinspection SpellCheckingInspection
class DiscordView:
    """
    Classe responsável pela View.
    Apresentação de comandos e ficheiros para os utilizadores e administradores.
    """

    # noinspection SpellCheckingInspection
    def __init__(self, bot):
        """
        Inicializa a view do Discord.
        
        """
        self.bot = bot
        self.controller = UserController()
        self.bot.controller = BotController()
        self.data_dir = Path("dados/puc")
        self.admin_checker = AdminChecker()
        self.consulta_model = ConsultaModel()
        self.logger = bot_logger

        # Regista listeners do bot controller
        self.bot.controller.adicionar_listener_estatisticas_acedidas(self._on_estatisticas_acedidas)
        self.bot.controller.adicionar_listener_relatorio_gerado(self._on_relatorio_gerado)
        self.bot.controller.adicionar_listener_grafico_gerado(self._on_grafico_gerado)
        self.bot.controller.adicionar_listener_erro(self._on_erro)

        self.logger.info("DiscordView inicializada com sucesso")

    async def processar_comando(self, ctx, command_name: str, *args) -> None:
        """
        Processa um comando recebido do Discord e envia para o controller apropriado.

        """
        try:
            self.logger.info(f"Comando recebido: {command_name} de {ctx.author.name} (ID: {ctx.author.id})")

            if command_name in self.controller.comandos_validos:
                await self._usar_comando_puc(ctx, command_name)
            elif command_name in ["relatorio", "estatisticas", "historico", "grafico_comandos", "grafico_seccoes"]:
                await self._usar_comando_administrador(ctx, command_name, *args)
            elif command_name in ["help", "ajuda"]:
                await self._usar_comando_help(ctx, *args)
            else:
                # Comando desconhecido - enviar mensagem informativa
                self.logger.warning(f"Comando não reconhecido: {command_name}")
                await ctx.send(f"O comando `!{command_name}` não foi reconhecido. Digite `!ajuda` para ver os comandos disponíveis.")

        except Exception as e:
            self.logger.error(f"Erro ao processar comando {command_name}: {str(e)}")
            await ctx.send(f"Erro ao processar o comando: {str(e)}")

    async def _usar_comando_puc(self, ctx, command_name: str) -> None:
        """
        Processa comandos relacionados à PUC.
        
        """
        dados = self.controller.processar_comando(ctx.author.id, ctx.author.name, command_name)
        
        # Verifica se o comando foi reconhecido
        if dados is None:
            await ctx.send(f"O comando `!{command_name}` não foi reconhecido. Digite `!ajuda` para ver os comandos disponíveis.")
            return
            
        resposta = self._formatar_resposta(command_name, dados)
        await self._enviar_resposta_formatada(ctx, command_name, resposta)
        self.logger.debug(f"Comando {command_name} processado com sucesso")        
    
    async def _usar_comando_administrador(self, ctx, command_name: str, *args) -> None:
        """
        Processa comandos administrativos.
        
        """
        if not await self._verificar_premissoes_administrador(ctx):
            self.logger.warning(
                f"Tentativa de acesso não autorizado ao comando admin {command_name} por {ctx.author.name}")
            await ctx.send("Este comando é restrito a administradores.")
            return

        self.logger.info(f"A processar comando administrativo {command_name}")

        try:
            if command_name == "relatorio":
                report_file = await self.bot.controller.gerar_relatorio(str(ctx.author.id))
                await ctx.send("Aqui está o relatório solicitado:", file=report_file)
            elif command_name == "estatisticas":
                estatisticas = self.bot.controller.obter_estatisticas(str(ctx.author.id))
                await self._enviar_resposta_estatisticas(ctx, estatisticas)
            elif command_name == "historico":
                await self._usar_comando_historico(ctx, *args)
            elif command_name in ["grafico_comandos", "grafico_seccoes"]:
                await self._usar_comando_grafico(ctx, command_name)

            self.logger.debug(f"Comando administrativo {command_name} processado com sucesso")

        except Exception as e:
            self.logger.error(f"Erro ao processar comando administrativo {command_name}: {str(e)}")
            await ctx.send(f"Erro ao processar o comando: {str(e)}")

    async def _usar_comando_historico(self, ctx, *args) -> None:
        """
        Processa o comando de histórico.        
        
        """
        if not args:
            await ctx.send("Por favor, mencione um utilizador para ver o seu histórico.")
            return
        historico = self.bot.controller.obter_utilizador_historico(args[0], str(ctx.author.id))
        await self._enviar_resposta_historico_usuario(ctx, historico)

    async def _usar_comando_grafico(self, ctx, command_name: str) -> None:
        """
        Processa comandos de gráficos.        
       
        """
        if command_name == "grafico_comandos":
            graph_file = await self.bot.controller.gerar_grafico_comandos(str(ctx.author.id))
            await ctx.send("Aqui está o gráfico de comandos:", file=graph_file)
        elif command_name == "grafico_seccoes":
            graph_file = await self.bot.controller.gerar_grafico_seccoes(str(ctx.author.id))
            await ctx.send("Aqui está o gráfico de secções:", file=graph_file)

    async def _usar_comando_help(self, ctx, *args) -> None:
        """
        Processa o comando de ajuda.
        
        """
        if len(args) > 0:
            await self._enviar_comando_help(ctx, args[0])
            self.logger.debug(f"Ajuda específica enviada para comando {args[0]}")
        else:
            await self._enviar_comando_lista(ctx)
            self.logger.debug("Lista completa de comandos enviada")

    async def _enviar_resposta_estatisticas(self, ctx, stats: dict) -> None:
        """
        Envia uma resposta formatada com estatísticas.
        
        """
        try:
            formatted_stats = self._formatar_estatisticas_para_discord(stats)
            await self._enviar_resposta_formatada(ctx, "estatisticas", formatted_stats)
            self.logger.debug("Estatísticas enviadas com sucesso")

        except Exception as e:
            self.logger.error(f"Erro ao enviar estatísticas: {str(e)}")
            raise

    def _formatar_data(self, data_str):
        """
        Formata uma _string de data ISO para um formato legível.
        
        """
        if not data_str:
            return ""
        try:
            data_obj = datetime.fromisoformat(data_str)
            return data_obj.strftime('%d/%m/%Y %H:%M:%S')
        except (ValueError, TypeError):
            return data_str

    def _formatar_estatisticas_para_discord(self, estatisticas):
        """
        Formata as estatísticas para apresentação na _interface Discord.
        
        """
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
                    "itens": [f"{cmd}: {count} vezes" for cmd, count in estatisticas['comandos_populares'][:5]] or ["Nenhum comando registado"]
                },
                {
                    "titulo": "Top 5 Secções",
                    "itens": [f"{secao}: {count} vezes" for secao, count in estatisticas['seccoes_populares'][:5]] or ["Nenhuma secção registada"]
                },
                {
                    "titulo": "Top 5 Utilizadores",
                    # Mostra apenas o nome do utilizador, sem o _ID
                    "itens": [f"{nome}: {count} consultas" for uid, nome, count in estatisticas['utilizadores_ativos'][:5]] or ["Nenhum utilizador registado"]
                }
            ]
        }

    def _ler_ficheiro_puc(self, filename: str) -> str:
        """
        Lê o conteúdo de um ficheiro da pasta dados/puc.        
        """
        file_path = self.data_dir / f"{filename}.txt"
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                self.logger.debug(f"Ficheiro {filename}.txt lido com sucesso")
                return content
        except FileNotFoundError:
            self.logger.error(f"Ficheiro {filename}.txt não encontrado")
            return f"Ficheiro {filename} não encontrado."

    async def _enviar_resposta_formatada(self, ctx, command_name: str, content) -> None:
        """
        Envia uma resposta formatada para o Discord.
        Suporta conteúdo do tipo str, dict, list[str] e list[dict].
        """
        try:
            # Caso 1: dicionário com estrutura de seções
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
                self.logger.debug(f"Resposta estruturada enviada para comando {command_name}")
                return

            # Caso 2: lista de strings
            elif isinstance(content, list) and all(isinstance(item, str) for item in content):
                embed = discord.Embed(
                    title=f"Resultado: {command_name}",
                    description="\n".join(content),
                    color=discord.Color.blue()
                )
                await ctx.send(embed=embed)
                self.logger.debug(f"Lista de strings enviada para comando {command_name}")
                return

            # Caso 3: lista de dicionários
            elif isinstance(content, list) and all(isinstance(item, dict) for item in content):
                embed = discord.Embed(
                    title=f"Resultado: {command_name}",
                    color=discord.Color.blue()
                )
                for i, item in enumerate(content, 1):
                    embed.add_field(name=f"Item {i}", value="\n".join(f"**{k}:** {v}" for k, v in item.items()),
                                    inline=False)
                await ctx.send(embed=embed)
                self.logger.debug(f"Lista de dicionários enviada para comando {command_name}")
                return

            # Caso 4: string simples ou fallback
            if not isinstance(content, str):
                self.logger.warning(f"Tipo de conteúdo inesperado: {type(content)} — convertido para string.")
                content = str(content)

            lines = content.split('\n')
            title = lines[0].replace('#', '').strip() if lines else "Informação"
            description = '\n'.join(lines[1:]).strip() if len(lines) > 1 else ""

            embed = discord.Embed(
                title=title,
                description=description,
                color=discord.Color.blue()
            )
            await ctx.send(embed=embed)
            self.logger.debug(f"Texto simples enviado para comando {command_name}")

        except Exception as e:
            self.logger.error(f"Erro ao enviar resposta formatada: {str(e)}")
            raise

    async def _verificar_premissoes_administrador(self, ctx) -> bool:
        """
        Verifica se o utilizador tem permissões de administrador.
        
        """
        is_discord_admin = ctx.author.guild_permissions.administrator
        env_administrador = self.admin_checker.administrador(str(ctx.author.id))

        if env_administrador:
            self.logger.info(f"Utilizador {ctx.author.name} (ID: {ctx.author.id}) autenticado como admin via .env")
        elif is_discord_admin:
            self.logger.info(f"Utilizador {ctx.author.name} (ID: {ctx.author.id}) autenticado como admin via Discord")
        else:
            self.logger.warning(f"Utilizador {ctx.author.name} (ID: {ctx.author.id}) não tem permissões de administrador")

        return is_discord_admin or env_administrador

    async def _enviar_comando_help(self, ctx, command_name: str) -> None:
        """
        Envia ajuda sobre um comando específico.
        
        """
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

            command_descriptions = {
            command_decriptions = {
                "relatorio": "Gera um relatório completo de uso do bot em formato Markdown",
                "estatisticas": "Mostra um resumo das estatísticas de uso do bot",
                "historico": "Mostra o histórico de comandos de um utilizador específico",
                "grafico_comandos": "Gera um gráfico dos comandos mais utilizados",
                "grafico_seccoes": "Gera um gráfico das secções mais consultadas"
            }

            descricao = command_descriptions.get(command_name)
                "grafico_seccoes": "Gera um gráfico das seções mais consultadas"
            }

            descricao = command_decriptions.get(command_name)
            if descricao:
                embed.add_field(name="Descrição", value=descricao, inline=False)

        else:
            embed.description = "Comando não encontrado"

        await ctx.send(embed=embed)

    async def _enviar_comando_lista(self, ctx) -> None:
        """
        Envia a lista de comandos disponíveis.
        
        """
        administrador = await self._verificar_premissoes_administrador(ctx)

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
        if administrador:
            embed.add_field(
                name="Comandos Administrativos",
                value="\n".join([
                    "!relatorio - Gera relatório completo de uso",
                    "!estatisticas - Mostra estatísticas de uso",
                    "!historico @user - Histórico de um utilizador",
                    "!grafico_comandos - Gráfico dos comandos mais usados",
                    "!grafico_seccoes - Gráfico das secções mais consultadas"
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

    async def _enviar_resposta_historico_usuario(self, ctx, historico):
        """
        Envia o histórico de um utilizador ao Discord.
        
        """
        if not historico:
            await ctx.send("Este utilizador não tem histórico de consultas.")
            return

        usuario_nome = historico[0]['nome']
        embed = discord.Embed(
            title=f"Histórico de {usuario_nome}",
            description=f"Total de consultas: {len(historico)}",
            color=discord.Color.blue()
        )

        # Mostra as últimas 10 consultas
        consultas_recentes = sorted(historico, key=lambda x: x['data'], reverse=True)[:10]
        consultas_texto = []
        for consulta in consultas_recentes:
            data = self._formatar_data(consulta['data'])
            cmd = consulta['comando']
            secao = consulta.get('secao', 'N/A')
            consultas_texto.append(f"{data}: {cmd} / {secao}")

        embed.add_field(
            name="Consultas Recentes",
            value="\n".join(consultas_texto) if consultas_texto else "Nenhuma consulta registada",
            inline=False
        )

        await ctx.send(embed=embed)

    # === Event Handlers do Controller ===

    def _on_estatisticas_acedidas(self, admin_id: str, estatisticas: dict) -> None:
        """
        Handler para evento de estatísticas acedidas.
        
        """
        self.logger.info(f"Estatísticas acedidas por admin {admin_id}")

    def _on_relatorio_gerado(self, admin_id: str, tipo_relatorio: str, caminho_ficheiro: str) -> None:
        """
        Handler para evento de relatório gerado.
        
        """
        self.logger.info(f"Relatório {tipo_relatorio} gerado por admin {admin_id}: {caminho_ficheiro}")

    def _on_grafico_gerado(self, admin_id: str, tipo_grafico: str, caminho_ficheiro: str) -> None:
        """
        Handler para evento de gráfico gerado.
        
        """
        self.logger.info(f"Gráfico {tipo_grafico} gerado por admin {admin_id}: {caminho_ficheiro}")

    def _on_erro(self, admin_id: str, operacao: str, mensagem_erro: str) -> None:
        """
        Handler para evento de erro.
        
        """
        self.logger.error(f"Erro na operação {operacao} por admin {admin_id}: {mensagem_erro}")

    def _formatar_resposta(self, seccao, dados):
        """
        Formata a resposta com base na secção e nos dados obtidos.
        
        """
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
