from abc import ABC, abstractmethod

class IView(ABC):
    """Interface para views do sistema."""
    
    @abstractmethod
    async def processar_commando(self, ctx, command_name, *args):
        """Processa um comando recebido e o envia para o controlador adequado."""
        pass
    
    @abstractmethod
    async def send_response(self, ctx, content):
        """Envia uma resposta para o usuário."""
        pass