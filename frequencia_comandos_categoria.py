import dash
from dash import html, Input, Output, callback, State
import requests
import pandas as pd
import dash_bootstrap_components as dbc
from dash import dcc

# Registrar a página no Dash
dash.register_page(__name__, path='/frequencia_comandos_categoria')

# Layout da página
layout = html.Div([
    html.H2("Frequência de Comandos por Categoria"),

    # Botão para carregar dados
    html.Button(
        "Carregar Dados",
        id="btn-carregar-frequencia",
        className="btn btn-primary"
    ),

    # Botão para exportar para PDF
    html.Button(
        "Exportar para PDF",
        id="btn-exportar-pdf-frequencia",
        className="btn btn-success",
        style={'margin-left': '10px'}
    ),

    # Local onde a tabela será exibida
    html.Div(id="tabela-frequencia", style={'margin-top': '20px'}),

    # Componente necessário para permitir downloads
    dcc.Download(id="download-pdf-frequencia")
])


# Callback para carregar a tabela de frequência de comandos por categoria
@callback(
    Output("tabela-frequencia", "children"),
    Input("btn-carregar-frequencia", "n_clicks"),
    State("dropdown_fonte_dados", "value")
)
def carregar_dados(n_clicks, fonte):
    if n_clicks is None:
        return ""

    resposta = requests.get(f"http://127.0.0.1:5000/testar_conexao/{fonte}/frequencia_comandos_categoria")

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


# Callback para exportar a frequência de comandos para PDF
@callback(
    Output("download-pdf-frequencia", "data"),
    Input("btn-exportar-pdf-frequencia", "n_clicks"),
    prevent_initial_call=True
)
def exportar_frequencia_para_pdf(n_clicks):
    print("🚀 [DASH] Solicitando captura da frequência de comandos e geração do PDF...")

    # Chama o Flask para capturar a imagem e gerar o PDF
    resposta = requests.get("http://127.0.0.1:5000/gerar_pdf_frequencia")

    if resposta.status_code == 200:
        caminho_pdf = resposta.json().get("caminho_pdf", "")
        if caminho_pdf:
            return dcc.send_file(caminho_pdf)

    print("❌ [DASH] ERRO: Falha ao gerar o PDF da frequência de comandos!")
    raise dash.exceptions.PreventUpdate
