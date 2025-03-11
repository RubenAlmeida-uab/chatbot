import sys
from flask import Flask, jsonify, send_file
import plotly.express as px
import pandas as pd
import os
from fpdf import FPDF


# Adiciona o diretório raiz do projeto ao PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.conexao_mysql import obter_dados_mysql
from dados.carregar_dados import carregar_dados_csv

app = Flask(__name__)

@app.route('/testar_conexao/<string:fonte>/<string:tabela>', methods=['GET'])
def testar_conexao(fonte, tabela):
    print(f"🔵 Testando conexão | Fonte: {fonte}, Tabela: {tabela}")

    if fonte.lower() == 'mysql':
        print("📡 Obtendo dados do MySQL...")
        dados = obter_dados_mysql(tabela)
    elif fonte.lower() == 'csv':
        print("📂 Obtendo dados do CSV...")
        dados = carregar_dados_csv(tabela)
    else:
        print("❌ Fonte inválida!")
        return jsonify({"erro": "Fonte inválida. Use 'mysql' ou 'csv'."}), 400

    print(f"✅ Conexão bem-sucedida! Dados obtidos: {len(dados)} registros")
    return jsonify({"dados": dados})


# Diretório de exportação
# Diretório de exportação
EXPORT_FOLDER = os.path.join(os.getcwd(), "exportação_PDF")
if not os.path.exists(EXPORT_FOLDER):
    os.makedirs(EXPORT_FOLDER)

@app.route('/gerar_pdf', methods=['GET'])
def gerar_pdf():
    try:
        print("🚀 [FLASK] Iniciando geração do PDF...")

        # Criar dados fictícios para o gráfico
        df = pd.DataFrame({"Categoria": ["A", "B", "C"], "Valor": [10, 20, 30]})
        fig = px.bar(df, x="Categoria", y="Valor", title="Gráfico Teste")

        # Salvar o gráfico como PNG
        caminho_png = os.path.join(EXPORT_FOLDER, "grafico_teste.png")
        fig.write_image(caminho_png, format="png")

        if os.path.exists(caminho_png):
            print(f"✅ [FLASK] Gráfico salvo com sucesso: {caminho_png}")
        else:
            print("❌ [FLASK] ERRO: O gráfico não foi salvo corretamente!")

        # Criar o PDF
        caminho_pdf = os.path.join(EXPORT_FOLDER, "relatorio_graficos.pdf")
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 18)
        pdf.cell(200, 10, "Relatório de Distribuição de Carga Docente", ln=True, align="C")
        pdf.ln(10)

        # Adicionar a imagem ao PDF
        if os.path.exists(caminho_png):
            pdf.image(caminho_png, x=10, w=180)
            print("✅ [FLASK] Imagem adicionada ao PDF!")
        else:
            print("❌ [FLASK] ERRO: Imagem não encontrada!")

        pdf.output(caminho_pdf)

        if os.path.exists(caminho_pdf):
            print(f"✅ [FLASK] PDF gerado com sucesso: {caminho_pdf}")
            return send_file(caminho_pdf, as_attachment=True)
        else:
            print("❌ [FLASK] ERRO: PDF não foi gerado!")
            return jsonify({"erro": "Falha ao gerar o PDF."}), 500

    except Exception as e:
        print(f"❌ [FLASK] ERRO ao gerar PDF: {e}")
        return jsonify({"erro": str(e)}), 500

if __name__ == '__main__':
    print("🚀 Servidor Flask iniciado em http://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000, debug=True)