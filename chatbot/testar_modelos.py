# ============================================================
# testar_modelos.py - Testes aos modelos de dados e estatísticas
# ============================================================
# Unidade Curricular:
# Laboratório de Desenvolvimento de _Software_
#
# Autores:
# 🔹 Duarte Grilo
# 🔹 Rúben Almeida
# 🔹 Sofia Semedo
# 🔹 Yuran Eduardo
# 🔹 Carlos Costa
#
# Objetivo:
# Executar testes manuais aos modelos de dados:
# 🔹 ConsultaModel: registo e análise estatística
# 🔹 DadosModel: leitura de secções da unidade curricular
# ============================================================

from model.consulta_model import ConsultaModel
from model.dados_model import DadosModel
import os
from datetime import datetime

# ===============================
# Teste ao modelo ConsultaModel
# ===============================

def testar_modelo_consulta():
    print("🔍 Teste: ConsultaModel")

    consulta = ConsultaModel()

    # 1. Registar consulta real
    consulta.registar_consulta("001", "Ana", "ajuda", "competencias")
    print("✅ Consulta registada.")

    # 2. Ver estatísticas
    estatisticas = consulta.obter_estatisticas()
    print("📊 Estatísticas atuais:")
    for k, v in estatisticas.items():
        print(f"  {k}: {v}")

    # 3. Verificar ficheiro exportado
    data_hoje = datetime.now().strftime("%Y%m%d")
    caminho_json = f"estatistica/relatorios/estatisticas_{data_hoje}.json"
    if os.path.exists(caminho_json):
        print(f"📁 Estatísticas exportadas em: {caminho_json}")
    else:
        print("⚠️ Ficheiro de estatísticas não encontrado.")


# ===============================
# Teste ao modelo DadosModel
# ===============================


def testar_modelo_dados():
    print("\n🔍 Teste: DadosModel")

    dados = DadosModel()

    # 1. Ver secções disponíveis
    secoes = dados.obter_todas_seccoes()
    print(f"📄 Secções encontradas: {secoes}")

    # 2. Tentar ler 'competencias'
    conteudo = dados.obter_seccao("competencias")
    if conteudo:
        print("📘 Conteúdo de 'competencias':")
        print(conteudo.strip()[:300] + "..." if len(conteudo) > 300 else conteudo)
    else:
        print("❌ A secção 'competencias' não foi encontrada.")


# ===============================
# Execução dos testes
# ===============================


if __name__ == "__main__":
    testar_modelo_consulta()
    testar_modelo_dados()
