import logging
from model.dados_model import DadosModel
from model.consulta_model import ConsultaModel


class UserController:
    """
    Controlador para gerir as interações dos utilizadores com o chatbot.    
    """
    
    def __init__(self):
        """
        Inicializa o controlador com os modelos necessários e configura eventos.
        """
        self.dados_model = DadosModel()
        self.consulta_model = ConsultaModel()
        
        # Listeners para eventos do controlador
        self.listeners_comando_processado = []  # Eventos para quando um comando é processado
        self.listeners_seccao_acedida = []     # Eventos para quando uma secção é acedida
        self.listeners_erro = []               # Eventos para quando ocorre um erro
    
    # === Métodos para gerir eventos ===
    
    def adicionar_listener_comando_processado(self, listener):
        """
        Adiciona um listener para eventos de processamento de comandos.        
        """
        self.listeners_comando_processado.append(listener)
        self.logger.debug(f"Listener adicionado para comando processado: {listener.__name__ if hasattr(listener, '__name__') else 'anônimo'}")
    
    def adicionar_listener_seccao_acedida(self, listener):
        """
        Adiciona um listener para eventos de acesso a secções.        
        """
        self.listeners_seccao_acedida.append(listener)
        self.logger.debug(f"Listener adicionado para secção acedida: {listener.__name__ if hasattr(listener, '__name__') else 'anônimo'}")
    
    def adicionar_listener_erro(self, listener):
        """
        Adiciona um listener para eventos de erro.        
        """
        self.listeners_erro.append(listener)
        self.logger.debug(f"Listener adicionado para erro: {listener.__name__ if hasattr(listener, '__name__') else 'anônimo'}")
    
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
            self.logger.debug(f"Listener removido: {listener.__name__ if hasattr(listener, '__name__') else 'anônimo'}")
    
    # === Métodos para emitir eventos ===
    
    def _notificar_comando_processado(self, utilizador_id, utilizador_nome, comando, seccao, sucesso):
        """
        Notifica todos os listeners de processamento de comandos.        
        """
        if sucesso:
            self.logger.info(f"Comando '{comando}' processado com sucesso para {utilizador_nome} (ID: {utilizador_id})")
        else:
            self.logger.warning(f"Comando '{comando}' processado com falha para {utilizador_nome} (ID: {utilizador_id})")
            
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
        
    def processar_comando(self, utilizador_id, utilizador_nome, comando, seccao=None):
        """
        Processa um comando recebido pela View.        
        """
        self.logger.info(f"Recebido comando '{comando}' de {utilizador_nome} (ID: {utilizador_id})")
        
        # Lista de comandos válidos que este controlador pode processar
        comandos_validos = ["puc", "ajuda", "listar_seccoes", "unidade_curricular", 
                           "competencias", "roteiro", "metodologia", "recursos",
                           "calendario", "avaliacao", "exame", "ia", "estrutura", "cartao"]
        
        if comando in comandos_validos:
            # IMPORTANTE: Registra a consulta no modelo primeiro, independentemente do resultado
            # Este é o ponto crítico para garantir que as estatísticas sejam registradas
            self.logger.debug(f"Registrando consulta para comando '{comando}' de {utilizador_nome}")
            self.consulta_model.registar_consulta(utilizador_id, utilizador_nome, comando, seccao)
            
            # Processa o comando e obtém a resposta
            resposta = self.obter_resposta(utilizador_id, utilizador_nome, comando, seccao)
            return resposta
        else:
            self.logger.debug(f"Comando '{comando}' não é processado por este controlador")
            return None  # Indica que este controlador não processou o comando
    
    def obter_resposta(self, utilizador_id, utilizador_nome, comando, seccao=None):
        """
        Obtém uma resposta para o comando do utilizador.        
        """
        try:
            # Processa o comando e obtém a resposta
            if seccao:
                self.logger.debug(f"Buscando secção '{seccao}' para comando '{comando}'")
                dados_seccao = self.dados_model.obter_seccao(seccao.lower())
                if dados_seccao:
                    # Notifica listeners que uma secção foi acedida com sucesso
                    self._notificar_seccao_acedida(utilizador_id, seccao, dados_seccao)
                    
                    # Notifica que o comando foi processado com sucesso
                    self._notificar_comando_processado(utilizador_id, utilizador_nome, comando, seccao, True)
                    
                    return self._formatar_resposta(seccao, dados_seccao)
                else:
                    # Notifica erro - secção não encontrada
                    erro_msg = f"Secção '{seccao}' não encontrada"
                    self.logger.warning(erro_msg)
                    self._notificar_erro(utilizador_id, comando, seccao, erro_msg)
                    
                    # Notifica que o comando foi processado mas com falha
                    self._notificar_comando_processado(utilizador_id, utilizador_nome, comando, seccao, False)
                    
                    return f"Desculpe, não encontrei informações sobre '{seccao}' no PUC."
            else:
                # Comando para listar todas as secções
                if comando == "listar_seccoes":
                    self.logger.debug("Listando todas as secções disponíveis")
                    seccoes = self.dados_model.obter_todas_seccoes()
                    
                    # Notifica que o comando foi processado com sucesso
                    self._notificar_comando_processado(utilizador_id, utilizador_nome, comando, None, True)
                    
                    return "**Secções disponíveis no PUC:**\n" + "\n".join([f"- {seccao}" for seccao in seccoes])
                # Comando de ajuda
                elif comando == "ajuda":
                    self.logger.debug("Fornecendo mensagem de ajuda")
                    # Notifica que o comando foi processado com sucesso
                    self._notificar_comando_processado(utilizador_id, utilizador_nome, comando, None, True)
                    
                    return self._obter_ajuda()
                # Comando PUC
                elif comando == "puc":
                    self.logger.debug("Fornecendo visão geral do PUC")
                    # Notifica que o comando foi processado com sucesso
                    self._notificar_comando_processado(utilizador_id, utilizador_nome, comando, None, True)
                    
                    return self._obter_puc_geral()
                # Outros comandos específicos sem secção
                elif comando in ["unidade_curricular", "competencias", "roteiro", "metodologia", 
                               "recursos", "avaliacao", "calendario", "exame", "ia", 
                               "estrutura", "cartao"]:
                    self.logger.debug(f"Tratando comando '{comando}' como secção")
                    # Trata o comando como se fosse uma secção
                    return self.obter_resposta(utilizador_id, utilizador_nome, "puc", comando)
                # Comando não reconhecido
                else:
                    # Notifica erro - comando não reconhecido
                    erro_msg = f"Comando '{comando}' não reconhecido"
                    self.logger.warning(erro_msg)
                    self._notificar_erro(utilizador_id, comando, None, erro_msg)
                    
                    # Notifica que o comando foi processado mas com falha
                    self._notificar_comando_processado(utilizador_id, utilizador_nome, comando, None, False)
                    
                    return "Comando não reconhecido. Digite `!ajuda` para ver os comandos disponíveis."
        except Exception as e:
            # Notifica erro - exceção durante processamento
            erro_msg = f"Erro ao processar comando: {str(e)}"
            self.logger.critical(f"Exceção ao processar comando '{comando}': {str(e)}")
            self._notificar_erro(utilizador_id, comando, seccao, erro_msg)
            
            # Notifica que o comando falhou
            self._notificar_comando_processado(utilizador_id, utilizador_nome, comando, seccao, False)
            
            # Retorna mensagem de erro genérica
            return "Ocorreu um erro ao processar o seu comando. Por favor, tente novamente mais tarde."
    
    def _formatar_resposta(self, seccao, dados):
        """
        Formata a resposta com base na secção e nos dados obtidos.        
        """
        self.logger.debug(f"Formatando resposta para secção '{seccao}'")
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
    
    def _obter_puc_geral(self):
        """
        Retorna uma visão geral do PUC.
        """
        self.logger.debug("Obtendo visão geral do PUC")
        puc_geral = """
# 📚 Plano da Unidade Curricular (PUC) 📚

Este é o plano geral da unidade curricular de Laboratório de Desenvolvimento de Software.

## Descrição Geral
LDS é uma unidade curricular focada na aplicação prática de conceitos de engenharia de software em projetos reais.

## Tópicos Principais
- Desenvolvimento de software em equipa
- Metodologias ágeis
- Gestão de projetos de software
- Práticas de codificação e teste
- Integração e entrega contínua

Para informações específicas, consulte as secções com `!listar_seccoes` ou peça ajuda com `!ajuda`.
        """
        return puc_geral
    
    def _obter_ajuda(self):
        """
        Retorna a mensagem de ajuda com os comandos disponíveis.        
        """
        self.logger.debug("Obtendo mensagem de ajuda")
        ajuda = """
# 📚 Bot LDS - Comandos Disponíveis 📚

## Informações Gerais
`!puc` - Visão geral do Plano da Unidade Curricular
`!unidade_curricular` - Descrição detalhada da disciplina
`!listar_seccoes` - Lista todas as secções disponíveis para consulta

## Conteúdo Académico
`!competencias` - Competências a desenvolver na disciplina
`!roteiro` - Roteiro completo do conteúdo a trabalhar
`!metodologia` - Métodos de trabalho e aprendizagem

## Organização da Disciplina
`!estrutura` - Como formar e organizar as equipas da SimProgramming
`!recursos` - Bibliografia e outros recursos recomendados
`!ia` - Diretrizes para utilização de ferramentas de inteligência artificial

## Avaliação
`!avaliacao` - Informações gerais sobre o processo de avaliação
`!cartao` - Detalhes sobre o Cartão de Aprendizagem
`!calendario` - Calendário completo de avaliação contínua
`!exame` - Informações sobre o exame final

Digite o comando para obter informações detalhadas sobre o tópico!
        """
        return ajuda
