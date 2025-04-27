import os

class DadosModel:
    def __init__(self, base_dir="dados/puc"):
        self.base_dir = base_dir

    def obter_seccao(self, nome):
        try:
            with open(f"{self.base_dir}/{nome}.txt", "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return None

    def obter_todas_seccoes(self):
        return [f.replace(".txt", "") for f in os.listdir(self.base_dir) if f.endswith(".txt")]
