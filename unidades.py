import dash
from dash import html, Input, Output, callback, State
import requests
import pandas as pd
import dash_bootstrap_components as dbc
from dash import dcc

# Registrar a página no Dash
dash.register_page(__name__, path='/unidades')

# Layout da página
layout = html.Div([
    html.H2("Tabela de Unidades Curriculares"),

    # Botão para carregar dados
    html.Button(
        "Carregar Dados",
        id="btn-carregar-unidades",
        className="btn btn-primary"
    ),

    # Botão para exportar unidades curriculares para PDF
    html.Button(
        "Exportar para PDF",
        id="btn-exportar-pdf",
        className="btn btn-success",
        style={'margin-left': '10px'}
    ),

    # Local onde a tabela será exibida
    html.Div(id="tabela-unidades", style={'margin-top': '20px'}),

    # Componente necessário para permitir downloads
    dcc.Download(id="download-pdf-unidades")
])


# Callback para carregar a tabela de unidades curriculares
@callback(
    Output("tabela-unidades", "children"),
    Input("btn-carregar-unidades", "n_clicks"),
    State("dropdown_fonte_dados", "value")
)
def carregar_dados(n_clicks, fonte):
    if n_clicks is None:
        return ""

    resposta = requests.get(f"http://127.0.0.1:5000/testar_conexao/{fonte}/unidades_curriculares")

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


# Callback para exportar unidades curriculares para PDF
@callback(
    Output("download-pdf-unidades", "data"),
    Input("btn-exportar-pdf", "n_clicks"),
    prevent_initial_call=True
)
def exportar_unidades_para_pdf(n_clicks):
    print("🚀 [DASH] Solicitando captura das unidades curriculares e geração do PDF...")

    # Chama o Flask para capturar a imagem e gerar o PDF
    resposta = requests.get("http://127.0.0.1:5000/gerar_pdf_unidades")

    if resposta.status_code == 200:
        caminho_pdf = resposta.json().get("caminho_pdf", "")
        if caminho_pdf:
            return dcc.send_file(caminho_pdf)

    print("❌ [DASH] ERRO: Falha ao gerar o PDF das unidades curriculares!")
    raise dash.exceptions.PreventUpdate

