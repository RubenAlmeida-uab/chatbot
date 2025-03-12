import pandas as pd
import os
from backend.config import CSV_FILES


def carregar_dados_csv(nome_tabela):
    caminho_csv = f"dados/arquivos_csv/{nome_tabela}.csv"

    codificacoes = ["utf-8", "utf-8-sig", "latin1", "iso-8859-1", "cp1252"]

    for encoding in codificacoes:
        try:
            df = pd.read_csv(caminho_csv, encoding=encoding, delimiter=",")
            print(f"✅ Arquivo '{nome_tabela}' carregado com sucesso usando encoding: {encoding}")
            return df.to_dict(orient="records")  # Retorna os dados formatados para JSON
        except UnicodeDecodeError:
            print(f"⚠️ Falha ao carregar '{nome_tabela}' com encoding: {encoding}, tentando outro...")

    print(f"❌ Nenhuma codificação funcionou para '{nome_tabela}'")
    return []
