import io
import os
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import discord
from model.consulta_model import ConsultaModel



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
        self.listeners_relatorio_gerado = []       # Eventos para quando relatórios são gerados
        self.listeners_grafico_gerado = []         # Eventos para quando gráficos são gerados
        self.listeners_erro = []                   # Eventos para quando ocorre um erro
    
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
                return self._formatar_estatisticas_para_discord(estatisticas)
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
    
    #este método que deve ser usado na view mas tb é usado para gerar os relatórios
    #deverá ser passado para utils
    def _formatar_data(self, data_str):
        """
        Formata uma string de data ISO para um formato legível.
        NOTA: Idealmente, esta funcionalidade deveria estar na View,
        mas será mantida aqui para suportar os métodos de geração de relatórios.
        ou passar para utils
        """
        if not data_str:
            return ""
            
        try:
            data_obj = datetime.fromisoformat(data_str)
            return data_obj.strftime('%d/%m/%Y %H:%M:%S')
        except (ValueError, TypeError):
            return data_str
    
    #metodo de formatação que deverá ser feita na view
    def _formatar_estatisticas_para_discord(self, estatisticas):
        """
        Formata as estatísticas para apresentação na interface Discord.
        """
        # Formata datas usando o método auxiliar
        primeiro_acesso = self._formatar_data(estatisticas.get('primeiro_acesso', ''))
        ultimo_acesso = self._formatar_data(estatisticas.get('ultimo_acesso', ''))
        
        resultado = {
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
                    "itens": [f"{nome} (ID: {uid}): {count} consultas" for uid, nome, count in estatisticas['utilizadores_ativos'][:5]] or ["Nenhum usuário registrado"]
                }
            ]
        }
        return resultado
    
    async def gerar_relatorio(self, admin_id=None):
        """
        Gera um relatório com estatísticas de uso do bot.        
        """
        try:
            estatisticas = self.obter_estatisticas()
            
            # Formata as datas usando o método auxiliar
            primeiro_acesso = self._formatar_data(estatisticas.get('primeiro_acesso', ''))
            ultimo_acesso = self._formatar_data(estatisticas.get('ultimo_acesso', ''))
            
            # Cria o conteúdo do relatório
            conteudo = [
                "# Relatório de Uso do Bot LDS\n",
                f"Data de geração: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n",
                f"Período: {primeiro_acesso} até {ultimo_acesso}\n\n",
                f"Total de consultas: {estatisticas['total_consultas']}\n",
                f"Utilizadores únicos: {estatisticas['utilizadores_unicos']}\n\n",
                "## Comandos mais populares\n"
            ]
            
            # Adiciona comandos populares
            if estatisticas['comandos_populares']:
                for comando, contagem in estatisticas['comandos_populares']:
                    conteudo.append(f"- {comando}: {contagem} consultas\n")
            else:
                conteudo.append("- Nenhum comando registrado\n")
            
            # Adiciona secções populares
            conteudo.append("\n## Secções mais consultadas\n")
            if estatisticas['seccoes_populares']:
                for seccao, contagem in estatisticas['seccoes_populares']:
                    conteudo.append(f"- {seccao}: {contagem} consultas\n")
            else:
                conteudo.append("- Nenhuma secção registrada\n")
            
            # Adiciona utilizadores ativos
            conteudo.append("\n## Utilizadores mais ativos\n")
            if estatisticas['utilizadores_ativos']:
                for utilizador_id, nome, contagem in estatisticas['utilizadores_ativos']:
                    conteudo.append(f"- {nome} (ID: {utilizador_id}): {contagem} consultas\n")
            else:
                conteudo.append("- Nenhum utilizador registrado\n")
            
            # Cria um ficheiro temporário com o relatório
            filename = f"relatorio_bot_lds_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"  # pode ser tb txt
            
            # Garante que o diretório exista
            os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)
            
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
                
                # Salva o gráfico
                filename = f"grafico_comandos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                fig.savefig(filename)
                
                if admin_id:
                    self._notificar_grafico_gerado(admin_id, "grafico_comandos", filename)
                
                return discord.File(filename)
            
            # Extrai dados para o gráfico
            comandos, contagens = zip(*estatisticas['comandos_populares']) if estatisticas['comandos_populares'] else ([], [])
            
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
                
                # Salva o gráfico
                filename = f"grafico_seccoes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                fig.savefig(filename)
                
                if admin_id:
                    self._notificar_grafico_gerado(admin_id, "grafico_seccoes", filename)
                
                return discord.File(filename)
            
            # Extrai dados para o gráfico
            seccoes, contagens = zip(*estatisticas['seccoes_populares']) if estatisticas['seccoes_populares'] else ([], [])            
            
            # Cria a figura e o gráfico
            fig = Figure(figsize=(10, 6))
            ax = fig.add_subplot(111)            
            
            ax.bar(seccoes, contagens, color='green')
            ax.set_xlabel('Secções')
            ax.set_ylabel('Número de consultas')
            ax.set_title('Secções mais consultadas')
            plt.setp(ax.get_xticklabels(), rotation=45, ha='right')            
            fig.tight_layout()
            
            # Salva o gráfico como imagem
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
        Obtém o histórico de consultas de um utilizador específico.        .
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
    
           
