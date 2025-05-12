from abc import ABC, abstractmethod

class IModel(ABC):
    """Interface para modelos do sistema."""
    
    @abstractmethod
    def carregar_dados(self):
        """Carrega os dados necessários para o modelo."""
        pass
    
    @abstractmethod
    def guardar_dados(self):
        """Guarda os dados do modelo."""
        pass