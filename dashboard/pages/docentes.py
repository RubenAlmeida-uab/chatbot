import dash
from dash import html, Input, Output, callback, State
import requests
import pandas as pd
import dash_bootstrap_components as dbc
from dash import dcc
import time
from dash.exceptions import PreventUpdate
import os




dash.register_page(__name__, path='/docentes')

layout = html.Div([
    html.H2("Tabela de Docentes"),


    # Botão para carregar dados
    html.Button(
        "Carregar Dados",
        id="btn-carregar-docentes",
        className="btn btn-primary"
    ),

    # Botão para exportar gráficos para PDF
    html.Button(
        "Exportar Gráfico para PDF",
        id="btn-exportar-pdf-grafico",
        className="btn btn-success",
        style={'margin-left':'10px'}
    ),

    # Local onde a tabela será exibida
    html.Div(id="tabela-docentes", style={'margin-top':'20px'}),

    # Componente necessário para permitir downloads
    dcc.Download(id="download-pdf")
])


@callback(
    Output("tabela-docentes", "children"),
    Input("btn-carregar-docentes", "n_clicks"),
    State("dropdown_fonte_dados", "value")
)
def carregar_dados(n_clicks, fonte):
    if n_clicks is None:
        return ""

    resposta = requests.get(f"http://127.0.0.1:5000/testar_conexao/{fonte}/tabela_docentes")

    if resposta.status_code == 200:
        dados = resposta.json()["dados"]
        if dados:
            df = pd.DataFrame(dados)
            return html.Div([
                dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
            ])
        else:
            return "Nenhum dado encontrado!"
    else:
        return f"Erro ao buscar dados: {resposta.status_code}"



# Callback para exportar gráficos para PDF
@dash.callback(
    Output("download-pdf", "data"),
    Input("btn-exportar-pdf-grafico", "n_clicks"),
    prevent_initial_call=True
)
def exportar_pdf(n_clicks):
    if not n_clicks:
        raise PreventUpdate

    print("🚀 [DASH] Solicitando geração do PDF ao Flask...")

    resposta = requests.get("http://127.0.0.1:5000/gerar_pdf")

    if resposta.status_code == 200:
        caminho_pdf = os.path.abspath("exportação_PDF/relatorio_graficos.pdf")  # Caminho correto do PDF
        print(f"📂 [DASH] Verificando caminho do PDF: {caminho_pdf}")

        # Aguarda o arquivo ser criado
        for _ in range(5):
            if os.path.exists(caminho_pdf):
                print("✅ [DASH] Arquivo encontrado! Enviando para download...")
                return dcc.send_file(caminho_pdf)
            time.sleep(1)

    print("❌ [DASH] ERRO: PDF não foi gerado pelo Flask!")
    raise PreventUpdate







