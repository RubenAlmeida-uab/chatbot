# ========================================================================
# bot_controller.py - Controlador Administrativo do Chatbot Discord
# ========================================================================
# Unidade Curricular:
# Laboratório de Desenvolvimento de _Software
#
# Objetivo:
# Este módulo implementa o _`BotController_`, responsável por gerir
# funcionalidades administrativas do chatbot, incluindo:
# 🔹 Geração e exportação de relatórios
# 🔹 Extração de estatísticas de uso
# 🔹 Criação de gráficos com base em dados de utilização
# 🔹 Gestão de histórico de utilizadores
# 🔹 Notificação de eventos (estatísticas, relatórios, erros, gráficos)
#
# Características Técnicas:
# - _Integra com o _`ConsultaModel_` para recolha de dados
# - Gera relatórios _`.md_` e gráficos _`.png_`
# - Produz ficheiros utilizáveis diretamente no Discord
# - Permite comunicação reativa _através de listeners
#
# Notas:
# - Usa _`matplotlib_` para gráficos e _`discord._File_` para envios
# - Compatível com _interface _`IController`
# ========================================================================

import os
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import discord
from model.consulta_model import ConsultaModel
from interfaces import IController


class BotController(IController):
    """
    Controlador para gerir as funções administrativas do _bot.
    """

    def __init__(self):
        """
        Inicializa o controlador com os modelos necessários e configura eventos.
        """
        self.consulta_model = ConsultaModel()

        # Listeners para eventos do controlador
        self.listeners_estatisticas_acedidas = []
        self.listeners_relatorio_gerado = []
        self.listeners_grafico_gerado = []
        self.listeners_erro = []

    # === Métodos da interface IController ===

    def adicionar_listener(self, tipo_evento, listener):
        """
        Adiciona um listener para um tipo específico de evento.                
        """
        if tipo_evento == "estatisticas_acedidas":
            self.listeners_estatisticas_acedidas.append(listener)
        elif tipo_evento == "relatorio_gerado":
            self.listeners_relatorio_gerado.append(listener)
        elif tipo_evento == "grafico_gerado":
            self.listeners_grafico_gerado.append(listener)
        elif tipo_evento == "erro":
            self.listeners_erro.append(listener)
        else:
            raise ValueError(f"Tipo de evento não suportado: {tipo_evento}")

    def remover_listener(self, listener):
        """
        Remove um listener de todas as listas de eventos.       
        """
        if listener in self.listeners_estatisticas_acedidas:
            self.listeners_estatisticas_acedidas.remove(listener)
        if listener in self.listeners_relatorio_gerado:
            self.listeners_relatorio_gerado.remove(listener)
        if listener in self.listeners_grafico_gerado:
            self.listeners_grafico_gerado.remove(listener)
        if listener in self.listeners_erro:
            self.listeners_erro.remove(listener)

    def processar_comando(self, utilizador_id, utilizador_nome, comando, *args):
        """
        Processa _comandos administrativo recebidoa pela View.
        """
        return self.processar_comando_admin(utilizador_id, comando, *args)

    # === Métodos para compatibilidade retroativa com código existente ===
    # mantidos para compatibilidade e redirecionam para o método da _interface

    def adicionar_listener_estatisticas_acedidas(self, listener):
        """
        Adiciona um listener para eventos de acesso a estatísticas.
        Redireciona para o método da _interface para evitar duplicação.
        """
        self.adicionar_listener("estatisticas_acedidas", listener)

    def adicionar_listener_relatorio_gerado(self, listener):
        """
        Adiciona um listener para eventos de geração de relatórios.
        Redireciona para o método da _interface para evitar duplicação.
        """
        self.adicionar_listener("relatorio_gerado", listener)

    def adicionar_listener_grafico_gerado(self, listener):
        """
        Adiciona um listener para eventos de geração de gráficos.
        Redireciona para o método da _interface para evitar duplicação.
        """
        self.adicionar_listener("grafico_gerado", listener)

    def adicionar_listener_erro(self, listener):
        """
        Adiciona um listener para eventos de erro.
        Redireciona para o método da _interface para evitar duplicação.
        """
        self.adicionar_listener("erro", listener)

    # === Métodos para emitir eventos ===

    def _notificar_estatisticas_acedidas(self, admin_id, estatisticas):
        """
        Notifica todos os listeners de acesso a estatísticas.        
        """
        for listener in self.listeners_estatisticas_acedidas:
            try:
                listener(admin_id, estatisticas)
            except Exception as e:
                print(f"Erro ao notificar listener: {e}")

    def _notificar_relatorio_gerado(self, admin_id, tipo_relatorio, caminho_ficheiro):
        """
        Notifica todos os listeners da geração de relatórios.        
        """
        for listener in self.listeners_relatorio_gerado:
            try:
                listener(admin_id, tipo_relatorio, caminho_ficheiro)
            except Exception as e:
                print(f"Erro ao notificar listener: {e}")

    def _notificar_grafico_gerado(self, admin_id, tipo_grafico, caminho_ficheiro):
        """
        Notifica todos os listeners de geração de gráficos.        
        """
        for listener in self.listeners_grafico_gerado:
            try:
                listener(admin_id, tipo_grafico, caminho_ficheiro)
            except Exception as e:
                print(f"Erro ao notificar listener: {e}")

    def _notificar_erro(self, admin_id, operacao, mensagem_erro):
        """
        Notifica todos os listeners de erro.        
        """
        for listener in self.listeners_erro:
            try:
                listener(admin_id, operacao, mensagem_erro)
            except Exception as e:
                print(f"Erro ao notificar listener: {e}")

    # === Métodos para processar comandos da View ===

    async def processar_comando_admin(self, admin_id, nome, comando, *args):
        """
        Processa um comando administrativo recebido pela View.       
        """
        try:
            if comando == "estatisticas":
                estatisticas = self.obter_estatisticas(admin_id)
                self.consulta_model.registar_consulta_admin(admin_id, nome, comando)
                self._notificar_estatisticas_acedidas(admin_id, estatisticas)
                return estatisticas
            elif comando == "relatorio":
                ficheiro = await self.gerar_relatorio(admin_id)
                return ficheiro
            elif comando == "grafico_comandos":
                ficheiro = await self.gerar_grafico_comandos(admin_id)
                return ficheiro
            elif comando == "grafico_seccoes":
                ficheiro = await self.gerar_grafico_seccoes(admin_id)
                return ficheiro
            elif comando == "historico" and len(args) > 0:
                utilizador_id = args[0]
                historico = self.obter_utilizador_historico(utilizador_id, admin_id)
                return historico
            elif comando == "ajuda":
                return "Comandos disponíveis: estatisticas, relatorio, grafico_comandos, grafico_seccoes, historico"
            else:
                self._notificar_erro(admin_id, comando, f"Comando não reconhecido: {comando}")
                return None  # Comando não reconhecido
        except Exception as e:
            self._notificar_erro(admin_id, comando, str(e))
            raise  # Reenvia a exceção para ser tratada na camada superior

    def obter_estatisticas(self, admin_id=None):
        """
        Obtém estatísticas de uso do bot.        
        """
        try:
            estatisticas = self.consulta_model.obter_estatisticas()

            # Se admin_id for fornecido, notifica os listeners
            if admin_id:
                self._notificar_estatisticas_acedidas(admin_id, estatisticas)

            return estatisticas
        except Exception as e:
            if admin_id:
                self._notificar_erro(admin_id, "obter_estatisticas", str(e))
            raise

    async def gerar_relatorio(self, admin_id=None):
        """
        Gera um relatório com estatísticas de uso do _bot.
        
        """
        try:
            estatisticas = self.obter_estatisticas()

            # Gera o conteúdo do relatório
            conteudo = self._gerar_conteudo_relatorio(estatisticas)

            # Define o caminho correto para o diretório de relatórios
            pasta_relatorios = "estatistica/relatorios"
            os.makedirs(pasta_relatorios, exist_ok=True)

            # Cria um ficheiro temporário com o relatório
            filename = f"{pasta_relatorios}/relatorio_bot_lds_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            with open(filename, 'w', encoding='utf-8') as f:
                f.writelines(conteudo)

            # Notifica os listeners se admin_id for fornecido
            if admin_id:
                self._notificar_relatorio_gerado(admin_id, "relatorio_geral", filename)

            # Retorna o ficheiro para ser enviado pelo Discord
            return discord.File(filename)
        except Exception as e:
            if admin_id:
                self._notificar_erro(admin_id, "gerar_relatorio", str(e))
            raise

    def _gerar_conteudo_relatorio(self, estatisticas):
        """
        Gera o conteúdo do relatório com base nas estatísticas fornecidas.
        
        """
        conteudo = [
            "# Relatório de Uso do Bot LDS\n",
            f"Data de geração: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n",
            f"Período: {estatisticas['primeiro_acesso']} até {estatisticas['ultimo_acesso']}\n\n",
            f"Total de consultas: {estatisticas['total_consultas']}\n",
            f"Utilizadores únicos: {estatisticas['utilizadores_unicos']}\n\n",
            "## Comandos mais populares\n"
        ]

        # Adiciona comandos populares
        if estatisticas['comandos_populares']:
            for comando, contagem in estatisticas['comandos_populares']:
                conteudo.append(f"- {comando}: {contagem} consultas\n")
        else:
            conteudo.append("- Nenhum comando registado\n")

        conteudo.append("\n## Secções mais consultadas\n")
        if estatisticas['seccoes_populares']:
            for seccao, contagem in estatisticas['seccoes_populares']:
                conteudo.append(f"- {seccao}: {contagem} consultas\n")
        else:
            conteudo.append("- Nenhuma secção registada\n")

        # Adiciona utilizadores ativos
        conteudo.append("\n## Utilizadores mais ativos\n")
        if estatisticas['utilizadores_ativos']:
            for utilizador_id, nome, contagem in estatisticas['utilizadores_ativos']:
                conteudo.append(f"- {nome} (ID: {utilizador_id}): {contagem} consultas\n")
        else:
            conteudo.append("- Nenhum utilizador registado\n")

        return conteudo

    async def gerar_grafico_comandos(self, admin_id=None):
        """
        Gera um gráfico com os comandos mais populares.
        
        """
        try:
            estatisticas = self.obter_estatisticas()

            # Verifica se há dados para gerar o gráfico
            if not estatisticas['comandos_populares']:
                # Cria um gráfico vazio com mensagem
                fig = Figure(figsize=(10, 6))
                ax = fig.add_subplot(111)
                ax.text(0.5, 0.5, "Sem dados suficientes para gerar o gráfico",
                        horizontalalignment='center', verticalalignment='center',
                        transform=ax.transAxes, fontsize=14)
                ax.set_axis_off()

                # Guarda o gráfico
                filename = f"grafico_comandos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                fig.savefig(filename)

                if admin_id:
                    self._notificar_grafico_gerado(admin_id, "grafico_comandos", filename)

                return discord.File(filename)

            # Extrai dados para o gráfico
            comandos, contagens = zip(*estatisticas['comandos_populares'])

            # Cria a figura
            fig = Figure(figsize=(10, 6))
            ax = fig.add_subplot(111)

            # Gera o gráfico de barras
            ax.bar(comandos, contagens, color='blue')
            ax.set_xlabel('Comandos')
            ax.set_ylabel('Número de consultas')
            ax.set_title('Comandos mais populares')
            plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
            fig.tight_layout()

            # Guarda o gráfico como imagem
            filename = f"grafico_comandos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            fig.savefig(filename)

            # Notifica os listeners se admin_id for fornecido
            if admin_id:
                self._notificar_grafico_gerado(admin_id, "grafico_comandos", filename)

            # Retorna o ficheiro para ser enviado pelo Discord
            return discord.File(filename)
        except Exception as e:
            if admin_id:
                self._notificar_erro(admin_id, "gerar_grafico_comandos", str(e))
            raise

    async def gerar_grafico_seccoes(self, admin_id=None):
        """
        Gera um gráfico com as secções mais consultadas.
        
        """
        try:
            estatisticas = self.obter_estatisticas()

            # Verifica se há dados para gerar o gráfico
            if not estatisticas['seccoes_populares']:
                # Cria um gráfico vazio com mensagem
                fig = Figure(figsize=(10, 6))
                ax = fig.add_subplot(111)
                ax.text(0.5, 0.5, "Sem dados suficientes para gerar o gráfico",
                        horizontalalignment='center', verticalalignment='center',
                        transform=ax.transAxes, fontsize=14)
                ax.set_axis_off()

                # Guarda o gráfico
                filename = f"grafico_seccoes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                fig.savefig(filename)

                if admin_id:
                    self._notificar_grafico_gerado(admin_id, "grafico_seccoes", filename)

                return discord.File(filename)

            # Extrai dados para o gráfico
            seccoes, contagens = zip(*estatisticas['seccoes_populares'])

            # Cria a figura e o gráfico
            fig = Figure(figsize=(10, 6))
            ax = fig.add_subplot(111)

            ax.bar(seccoes, contagens, color='green')
            ax.set_xlabel('Secções')
            ax.set_ylabel('Número de consultas')
            ax.set_title('Secções mais consultadas')
            plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
            fig.tight_layout()

            # Guarda o gráfico como imagem
            filename = f"grafico_seccoes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            fig.savefig(filename)

            if admin_id:
                self._notificar_grafico_gerado(admin_id, "grafico_seccoes", filename)

            # Retorna o ficheiro para ser enviado pelo Discord
            return discord.File(filename)
        except Exception as e:
            if admin_id:
                self._notificar_erro(admin_id, "gerar_grafico_seccoes", str(e))
            raise

    def obter_utilizador_historico(self, utilizador_id, admin_id=None):
        """
        Obtém o histórico de consultas de um utilizador específico.
        
        """
        try:
            historico = self.consulta_model.obter_historico_utilizador(utilizador_id)
            return historico
        except Exception as e:
            if admin_id:
                self._notificar_erro(admin_id, "obter_historico", str(e))
            raise
