# controller/bot_controller.py
import io
import os
from datetime import datetime
from model.consulta_model import ConsultaModel
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

class BotController:
    """
    Controlador para gerir as funções administrativas do bot.
    """

    def __init__(self):
        """
        Inicializa o controlador com os modelos necessários e configura eventos.
        """
        self.consulta_model = ConsultaModel()

        # Listeners para eventos do controlador
        self.listeners_estatisticas_acedidas = []  # Eventos para quando estatísticas são acedidas
        self.listeners_relatorio_gerado = []  # Eventos para quando relatórios são gerados
        self.listeners_grafico_gerado = []  # Eventos para quando gráficos são gerados
        self.listeners_erro = []  # Eventos para quando ocorre um erro

    # === Métodos para gerir eventos ===

    def adicionar_listener_estatisticas_acedidas(self, listener):
        """
        Adiciona um listener para eventos de acesso a estatísticas.
        """
        self.listeners_estatisticas_acedidas.append(listener)

    def adicionar_listener_relatorio_gerado(self, listener):
        """
        Adiciona um listener para eventos de geração de relatórios.
        """
        self.listeners_relatorio_gerado.append(listener)

    def adicionar_listener_grafico_gerado(self, listener):
        """
        Adiciona um listener para eventos de geração de gráficos.
        """
        self.listeners_grafico_gerado.append(listener)

    def adicionar_listener_erro(self, listener):
        """
        Adiciona um listener para eventos de erro.
        """
        self.listeners_erro.append(listener)

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
        Notifica todos os listeners de geração de relatórios.
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

    async def processar_comando_admin(self, admin_id, admin_nome, comando, *args):
        """
        Processa um comando administrativo recebido pela View.
        """
        try:
            if comando == "estatisticas":
                estatisticas = self.obter_estatisticas(admin_id)
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
            elif comando == "historico_utilizador" and len(args) > 0:
                utilizador_id = args[0]
                historico = self.obter_utilizador_historico(utilizador_id, admin_id)
                return historico
            elif comando == "ajuda":
                # Aqui adiciona a resposta esperada para o comando ajuda
                return "Comandos disponíveis: estatisticas, relatorio, grafico_comandos, grafico_seccoes, historico_utilizador"
            else:
                return None  # Comando não reconhecido
        except Exception as e:
            self._notificar_erro(admin_id, comando, str(e))
            raise  # Re-lança a exceção para ser tratada na camada superior

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
        Gera um relatório com estatísticas de uso do bot e retorna o caminho do ficheiro.
        """
        try:
            estatisticas = self.obter_estatisticas()

            # Cria o conteúdo do relatório
            conteudo = [
                "# Relatório de Uso do Bot LDS\n",
                f"Data de geração: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n",
                f"Período: {estatisticas['primeiro_acesso']} até {estatisticas['ultimo_acesso']}\n\n",
                f"Total de consultas: {estatisticas['total_consultas']}\n",
                f"Utilizadores únicos: {estatisticas['utilizadores_unicos']}\n\n",
                "## Comandos mais populares\n"
            ]

            for comando, contagem in estatisticas['comandos_populares']:
                conteudo.append(f"- {comando}: {contagem} consultas\n")

            conteudo.append("\n## Secções mais consultadas\n")
            for seccao, contagem in estatisticas['seccoes_populares']:
                conteudo.append(f"- {seccao}: {contagem} consultas\n")

            conteudo.append("\n## Utilizadores mais ativos\n")
            for utilizador_id, nome, contagem in estatisticas['utilizadores_ativos']:
                conteudo.append(f"- {nome} (ID: {utilizador_id}): {contagem} consultas\n")

            # Cria um ficheiro temporário com o relatório
            filename = f"relatorio_bot_lds_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"  # pode ser tb txt
            with open(filename, 'w', encoding='utf-8') as f:
                f.writelines(conteudo)

            # Notifica os listeners se admin_id for fornecido
            if admin_id:
                self._notificar_relatorio_gerado(admin_id, "relatorio_geral", filename)

            # Retorna o caminho do ficheiro
            return filename
        except Exception as e:
            if admin_id:
                self._notificar_erro(admin_id, "gerar_relatorio", str(e))
            raise

    async def gerar_grafico_comandos(self, admin_id=None):
        """
        Gera um gráfico com os comandos mais populares e retorna o caminho do ficheiro.
        """
        try:
            estatisticas = self.obter_estatisticas()
            comandos, contagens = zip(*estatisticas['comandos_populares']) if estatisticas[
                'comandos_populares'] else ([], [])

            # Cria a figura
            fig = Figure(figsize=(10, 6))
            ax = fig.add_subplot(111)

            # Gera o gráfico de barras
            ax.bar(comandos, contagens, color='blue')
            ax.set_xlabel('Comandos')
            ax.set_ylabel('Número de consultas')
            ax.set_title('Comandos mais populares')
            plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

            # Guarda a figura num buffer de bytes
            buf = io.BytesIO()
            FigureCanvas(fig).print_png(buf)
            buf.seek(0)

            # Cria um ficheiro temporário com o gráfico
            filename = f"grafico_comandos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            with open(filename, 'wb') as f:
                f.write(buf.getbuffer())

            # Notifica os listeners se admin_id for fornecido
            if admin_id:
                self._notificar_grafico_gerado(admin_id, "grafico_comandos", filename)

            # Retorna o caminho do ficheiro
            return filename
        except Exception as e:
            if admin_id:
                self._notificar_erro(admin_id, "gerar_grafico_comandos", str(e))
            raise

    async def gerar_grafico_seccoes(self, admin_id=None):
        """
        Gera um gráfico com as secções mais consultadas e retorna o caminho do ficheiro.
        """
        try:
            estatisticas = self.obter_estatisticas()
            seccoes, contagens = zip(*estatisticas['seccoes_populares']) if estatisticas[
                'seccoes_populares'] else ([], [])

            fig = Figure(figsize=(10, 6))
            ax = fig.add_subplot(111)

            ax.bar(seccoes, contagens, color='green')
            ax.set_xlabel('Secções')
            ax.set_ylabel('Número de consultas')
            ax.set_title('Secções mais consultadas')
            plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

            buf = io.BytesIO()
            FigureCanvas(fig).print_png(buf)
            buf.seek(0)

            filename = f"grafico_seccoes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            with open(filename, 'wb') as f:
                f.write(buf.getbuffer())

            if admin_id:
                self._notificar_grafico_gerado(admin_id, "grafico_seccoes", filename)

            # Retorna o caminho do ficheiro
            return filename
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

            # Poderia adicionar um evento específico para acesso ao histórico
            # mas por simplicidade, não adicionei

            return historico
        except Exception as e:
            if admin_id:
                self._notificar_erro(admin_id, "obter_historico", str(e))
            raise