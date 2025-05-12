from abc import ABC, abstractmethod

class IEventListener(ABC):
    """Interface para listeners de eventos do sistema."""
    
    @abstractmethod
    def on_evento(self, tipo_evento, *args, **kwargs):
        """Método chamado quando um evento ocorre."""
        pass