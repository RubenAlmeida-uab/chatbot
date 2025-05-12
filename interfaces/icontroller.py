from abc import ABC, abstractmethod

class IController(ABC):
    """Interface para controladores do sistema."""
    
    @abstractmethod
    def adicionar_listener(self, tipo_evento, listener):
        """Adiciona um listener para um tipo específico de evento."""
        pass
    
    @abstractmethod
    def remover_listener(self, listener):
        """Remove um listener de todas as listas de eventos."""
        pass
    
    @abstractmethod
    def processar_comando(self, utilizador_id, utilizador_nome, comando, *args):
        """Processa um comando recebido pela View."""
        pass