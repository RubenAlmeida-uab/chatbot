
from model.dados_model import DadosModel
from model.consulta_model import ConsultaModel
from utils.logger import bot_logger
from interfaces import IController


class UserController(IController):
    """
    Controlador para gerir as interações dos utilizadores com o chatbot.
    """

    def __init__(self):
        """
        Inicializa o controlador com os modelos necessários e configura eventos.
        """
        self.dados_model = DadosModel()
        self.consulta_model = ConsultaModel()
        self.logger = bot_logger
        self.comandos_validos = [
            "uc", "competencias", "roteiro", "metodologia", "recursos",
            "calendario", "avaliacao", "exame", "ia", "estrutura", "cartao"]

        # Listeners para eventos do controlador
        self.listeners_comando_processado = []
        self.listeners_seccao_acedida = []
        self.listeners_erro = []

    # === Métodos da interface IController ===

    def adicionar_listener(self, tipo_evento, listener):
        """ 
        Adiciona um listener para um tipo específico de evento.
        Implementação da interface IController.        
        """
        if tipo_evento == "comando_processado":
            self.listeners_comando_processado.append(listener)
            self.logger.debug(f"Listener adicionado para comando processado: {listener.__name__ if hasattr(listener, '__name__') else 'anónimo'}")
        elif tipo_evento == "seccao_acedida":
            self.listeners_seccao_acedida.append(listener)
            self.logger.debug(f"Listener adicionado para secção acedida: {listener.__name__ if hasattr(listener, '__name__') else 'anónimo'}")
        elif tipo_evento == "erro":
            self.listeners_erro.append(listener)
            self.logger.debug(f"Listener adicionado para erro: {listener.__name__ if hasattr(listener, '__name__') else 'anónimo'}")
        else:
            raise ValueError(f"Tipo de evento não suportado: {tipo_evento}")

    def remover_listener(self, listener):
        """
        Remove um listener de todas as listas de eventos.        
        """
        removed = False
        if listener in self.listeners_comando_processado:
            self.listeners_comando_processado.remove(listener)
            removed = True
        if listener in self.listeners_seccao_acedida:
            self.listeners_seccao_acedida.remove(listener)
            removed = True
        if listener in self.listeners_erro:
            self.listeners_erro.remove(listener)
            removed = True

        if removed:
            self.logger.debug(f"Listener removido: {listener.__name__ if hasattr(listener, '__name__') else 'anónimo'}")

    def processar_comando(self, utilizador_id, utilizador_nome, comando, seccao=None):
        """
        Processa um comando recebido pela View.              
        """
        self.logger.info(f"Recebido comando '{comando}' de {utilizador_nome} (ID: {utilizador_id})")

        # Lista de comandos válidos que este controlador pode processar
        if comando in self.comandos_validos:
            # Regista a consulta no modelo - este é o ponto central e único para registro de consultas
            self.logger.debug(f"A registar consulta para comando '{comando}' de {utilizador_nome}")
            self.consulta_model.registar_consulta(utilizador_id, utilizador_nome, comando, seccao)

            # Processa o comando e obtém a resposta
            resposta = self.obter_resposta(utilizador_id, utilizador_nome, comando, seccao)
            return resposta
        else:
            self.logger.debug(f"Comando '{comando}' não é processado por este controlador")
            return None  # Indica que este controlador não processou o comando

    # === Métodos mantidos por compatibilidade com código existente ===
    # Estes métodos redirecionam para o método padrão da interface

    def adicionar_listener_comando_processado(self, listener):
        """
        Adiciona um listener para eventos de processamento de comandos.
        Redireciona para o método da interface para evitar duplicação.     
        """
        self.adicionar_listener("comando_processado", listener)

    def adicionar_listener_seccao_acedida(self, listener):
        """
        Adiciona um listener para eventos de acesso a secções.        
        """
        self.adicionar_listener("seccao_acedida", listener)

    def adicionar_listener_erro(self, listener):
        """
        Adiciona um listener para eventos de erro.              
        """
        self.adicionar_listener("erro", listener)

    # === Métodos para emitir eventos ===

    def _notificar_comando_processado(self, utilizador_id, utilizador_nome, comando, seccao, sucesso):
        """
        Notifica todos os listeners de processamento de comandos.               
        """
        if sucesso:
            self.logger.info(f"Comando '{comando}' processado com sucesso para {utilizador_nome} (ID: {utilizador_id})")
        else:
            self.logger.warning(
                f"Comando '{comando}' processado com falha para {utilizador_nome} (ID: {utilizador_id})")

        for listener in self.listeners_comando_processado:
            try:
                listener(utilizador_id, utilizador_nome, comando, seccao, sucesso)
            except Exception as e:
                self.logger.error(f"Erro ao notificar listener de comando processado: {e}")

    def _notificar_seccao_acedida(self, utilizador_id, seccao, dados):
        """
        Notifica todos os listeners de acesso a secções.        
        """
        self.logger.info(f"Secção '{seccao}' acedida pelo utilizador {utilizador_id}")
        for listener in self.listeners_seccao_acedida:
            try:
                listener(utilizador_id, seccao, dados)
            except Exception as e:
                self.logger.error(f"Erro ao notificar listener de secção acedida: {e}")

    def _notificar_erro(self, utilizador_id, comando, seccao, mensagem_erro):
        """
        Notifica todos os listeners de erro.
    
        """
        self.logger.error(f"Erro ao processar comando '{comando}' para utilizador {utilizador_id}: {mensagem_erro}")
        for listener in self.listeners_erro:
            try:
                listener(utilizador_id, comando, seccao, mensagem_erro)
            except Exception as e:
                self.logger.critical(f"Erro ao notificar listener de erro: {e}")

    # === Método principal de processamento de comandos ===

    def obter_resposta(self, utilizador_id, utilizador_nome, comando, seccao=None):
        """
        Obtém uma resposta para o comando do utilizador.        
        """
        try:
            # Processa o comando e obtém a resposta
            if seccao:
                return self._processar_comando_com_seccao(utilizador_id, utilizador_nome, comando, seccao)
            else:
                return self._processar_comando_sem_seccao(utilizador_id, utilizador_nome, comando)
        except Exception as e:
            return self._processar_erro(utilizador_id, utilizador_nome, comando, seccao, e)

    # === Métodos auxiliares para processamento de comandos ===

    def _processar_comando_com_seccao(self, utilizador_id, utilizador_nome, comando, seccao):
        """
        Processa comandos que incluem uma secção específica.        
        """
        self.logger.debug(f"A procurar secção '{seccao}' para comando '{comando}'")
        dados_seccao = self.dados_model.obter_seccao(seccao.lower())
        
        if dados_seccao:
            # Notifica que uma secção foi acedida com sucesso
            self._notificar_seccao_acedida(utilizador_id, seccao, dados_seccao)
            # Notifica que o comando foi processado com sucesso
            self._notificar_comando_processado(utilizador_id, utilizador_nome, comando, seccao, True)
            return dados_seccao
        else:
            # Secção não encontrada - notifica erro
            erro_msg = f"Secção '{seccao}' não encontrada"
            self._notificar_erro(utilizador_id, comando, seccao, erro_msg)
            # Notifica que o comando foi processado mas com falha
            self._notificar_comando_processado(utilizador_id, utilizador_nome, comando, seccao, False)
            return f"Desculpe, não encontrei informações sobre '{seccao}' no PUC."

    def _processar_comando_sem_seccao(self, utilizador_id, utilizador_nome, comando):
        """
        Processa comandos sem secção específica.        
        """
        # Identifica o tipo de comando e delega para métodos específicos
        if comando == "listar_seccoes":
            return self._processar_listar_seccoes(utilizador_id, utilizador_nome, comando)
        elif comando == "ajuda":
            return self._processar_ajuda(utilizador_id, utilizador_nome, comando)
        elif comando == "uc":
            return self._processar_uc(utilizador_id, utilizador_nome, comando)
        elif comando in self.comandos_validos:
            # Trata o comando como se fosse uma secção
            return self.obter_resposta(utilizador_id, utilizador_nome, "uc", comando)
        else:
            return self._processar_comando_desconhecido(utilizador_id, utilizador_nome, comando)

    def _processar_listar_seccoes(self, utilizador_id, utilizador_nome, comando):
        """
        Processa o comando para listar todas as secções disponíveis.        
        """
        self.logger.debug("A listar todas as secções disponíveis")
        seccoes = self.dados_model.obter_todas_seccoes()
        # Notifica que o comando foi processado com sucesso
        self._notificar_comando_processado(utilizador_id, utilizador_nome, comando, None, True)
        return "**Secções disponíveis no PUC:**\n" + "\n".join([f"- {seccao}" for seccao in seccoes])

    def _processar_ajuda(self, utilizador_id, utilizador_nome, comando):
        """
        Processa o comando de ajuda.        
        """
        self.logger.debug("A fornecer mensagem de ajuda")
        # Notifica que o comando foi processado com sucesso
        self._notificar_comando_processado(utilizador_id, utilizador_nome, comando, None, True)
        return self._obter_ajuda()

    def _processar_uc(self, utilizador_id, utilizador_nome, comando):
        """
        Processa o comando UC para obter visão geral da unidade curricular.        
        """
        self.logger.debug("A fornecer visão geral da UC")
        dados_uc = self.dados_model.obter_seccao("uc")
        
        if dados_uc:
            # Notifica que o comando foi processado com sucesso
            self._notificar_comando_processado(utilizador_id, utilizador_nome, comando, None, True)
            return dados_uc
        else:
            erro_msg = "Ficheiro 'uc.txt' não encontrado"
            self.logger.warning(erro_msg)
            self._notificar_erro(utilizador_id, comando, None, erro_msg)
            return "Desculpe, não foi possível encontrar informações gerais sobre a UC."

    def _processar_comando_desconhecido(self, utilizador_id, utilizador_nome, comando):
        """
        Processa um comando não reconhecido.        
        """
        erro_msg = f"Comando '{comando}' não reconhecido"
        self.logger.warning(erro_msg)
        self._notificar_erro(utilizador_id, comando, None, erro_msg)
        # Notifica que o comando foi processado mas com falha
        self._notificar_comando_processado(utilizador_id, utilizador_nome, comando, None, False)
        return "Comando não reconhecido. Digite `!ajuda` para ver os comandos disponíveis."

    def _processar_erro(self, utilizador_id, utilizador_nome, comando, seccao, excecao):
        """
        Processa uma exceção ocorrida durante o processamento de um comando.       
        """
        erro_msg = f"Erro ao processar comando: {str(excecao)}"
        self.logger.critical(f"Exceção ao processar comando '{comando}': {str(excecao)}")
        self._notificar_erro(utilizador_id, comando, seccao, erro_msg)
        # Notifica que o comando falhou
        self._notificar_comando_processado(utilizador_id, utilizador_nome, comando, seccao, False)
        # Retorna mensagem de erro genérica
        return "Ocorreu um erro ao processar o seu comando. Por favor, tente novamente mais tarde."

   
