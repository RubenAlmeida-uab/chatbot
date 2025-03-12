import sys
from flask import Flask, jsonify
import time
import pyautogui
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


@app.route('/gerar_pdf_tabela', methods=['GET'])
def gerar_pdf_tabela():
    try:
        print("🚀 [FLASK] Capturando a tabela e gerando o PDF...")

        # 🔹 Aguardar um pequeno delay para garantir que a página esteja carregada
        time.sleep(2)

        # 🔹 Capturar a tela (Screenshot)
        caminho_png = os.path.join(EXPORT_FOLDER, "tabela_docentes.png")
        screenshot = pyautogui.screenshot()
        screenshot.save(caminho_png)

        if os.path.exists(caminho_png):
            print(f"✅ [FLASK] Screenshot da tabela salvo: {caminho_png}")
        else:
            print("❌ [FLASK] ERRO: Falha ao capturar a tabela!")
            return jsonify({"erro": "Falha ao capturar a imagem da tabela!"}), 500

        # 🔹 Criar o PDF
        caminho_pdf = os.path.join(EXPORT_FOLDER, "relatorio_docentes.pdf")
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 18)
        pdf.cell(200, 10, "Relatório da Tabela de Docentes", ln=True, align="C")
        pdf.ln(10)

        # 🔹 Adicionar a imagem ao PDF
        pdf.image(caminho_png, x=10, w=180)
        pdf.output(caminho_pdf)

        if os.path.exists(caminho_pdf):
            print(f"✅ [FLASK] PDF gerado com sucesso: {caminho_pdf}")
            return jsonify({"caminho_pdf": caminho_pdf})
        else:
            print("❌ [FLASK] ERRO: PDF não foi gerado!")
            return jsonify({"erro": "Falha ao gerar o PDF!"}), 500

    except Exception as e:
        print(f"❌ [FLASK] ERRO ao gerar PDF: {e}")
        return jsonify({"erro": str(e)}), 500


if __name__ == '__main__':
    print("🚀 Servidor Flask iniciado em http://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000, debug=True)