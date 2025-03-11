import pandas as pd
import os
from config import CSV_FILES

def carregar_dados_csv(nome_tabela):
    try:
        caminho = os.path.abspath(CSV_FILES[nome_tabela])
        print(f"Caminho absoluto CSV: {caminho}")  # Depuração no console
        dados = pd.read_csv(caminho)
        return dados.to_dict(orient='records')
    except Exception as e:
        print(f"Erro ao carregar CSV: {e}")
        return []
