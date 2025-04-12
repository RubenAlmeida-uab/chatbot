import markdown2
from weasyprint import HTML

def gerar_relatorio_html(md_path, html_path):
    with open(md_path, "r", encoding="utf-8") as f:
        html = markdown2.markdown(f.read())
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

def gerar_pdf(html_path, pdf_path):
    HTML(html_path).write_pdf(pdf_path)
