import os

class DadosModel:
    """
    Classe para acesso a dados da unidade curricular.
    Responsável por carregar informações das secções do PUC.
    """
    
    def __init__(self, base_dir="dados/puc"):
        """
        Inicializa o modelo de dados.
        
        """
        self.base_dir = base_dir

    def obter_seccao(self, nome):
        """
        Obtém o conteúdo de uma secção específica do PUC.
        
        """
        try:
            with open(f"{self.base_dir}/{nome}.txt", "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return None

    def obter_todas_seccoes(self):
        """
        Obtém a lista de todas as secções disponíveis.
        
        """
        return [f.replace(".txt", "") for f in os.listdir(self.base_dir) if f.endswith(".txt")]
