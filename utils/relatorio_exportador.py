import markdown2
from weasyprint import HTML
import json
from datetime import datetime
import os

def gerar_nomes_ficheiros(base_dir="estatistica/relatorios"):
    data_hoje = datetime.now().strftime("%Y%m%d")
    json_path = os.path.join(base_dir, f"estatisticas_{data_hoje}.json")
    md_path = os.path.join(base_dir, f"relatorio_{data_hoje}.md")
    pdf_path = os.path.join(base_dir, f"relatorio_{data_hoje}.pdf")
    return json_path, md_path, pdf_path


def gerar_relatorio_md(caminho_json, caminho_saida_md):
    with open(caminho_json, "r", encoding="utf-8") as f:
        dados = json.load(f)

    linhas = [
        "# 📊 Relatório de Utilização do Bot\n",
        f"**Data de Geração:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n",
        f"**Período:** {dados['primeiro_acesso']} até {dados['ultimo_acesso']}\n",
        f"**Total de Consultas:** {dados['total_consultas']}\n",
        f"**Utilizadores Únicos:** {dados['utilizadores_unicos']}\n\n",
        "## 🔹 Comandos Mais Populares\n"
    ]

    for comando, count in dados['comandos_populares']:
        linhas.append(f"- {comando}: {count} vezes")

    linhas.append("\n## 🔹 Secções Mais Consultadas")
    for seccao, count in dados['seccoes_populares']:
        linhas.append(f"- {seccao}: {count} vezes")

    linhas.append("\n## 🔹 Utilizadores Mais Ativos")
    for uid, nome, count in dados['utilizadores_ativos']:
        linhas.append(f"- {nome} (ID: {uid}): {count} comandos")

    with open(caminho_saida_md, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas))

    print(f"✅ Relatório gerado: {caminho_saida_md}")

def gerar_pdf_a_partir_md(md_path, pdf_path):
    with open(md_path, "r", encoding="utf-8") as f:
        html = markdown2.markdown(f.read())
    HTML(string=html).write_pdf(pdf_path)
    print(f"✅ PDF gerado em: {pdf_path}")
