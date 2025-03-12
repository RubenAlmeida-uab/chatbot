import dash
from dash import html, Input, Output, callback, State
import requests
import pandas as pd
import dash_bootstrap_components as dbc
from dash import dcc


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
        id="btn-exportar-pdf",
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
# Callback para capturar a tabela e gerar o PDF
@callback(
    Output("download-pdf", "data"),
    Input("btn-exportar-pdf", "n_clicks"),
    prevent_initial_call=True
)
def exportar_tabela_para_pdf(n_clicks):
    print("🚀 [DASH] Solicitando captura da tabela e geração do PDF...")

    # Chama o Flask para capturar a imagem e gerar o PDF
    resposta = requests.get("http://127.0.0.1:5000/gerar_pdf_tabela")

    if resposta.status_code == 200:
        caminho_pdf = resposta.json().get("caminho_pdf", "")
        if caminho_pdf:
            return dcc.send_file(caminho_pdf)

    print("❌ [DASH] ERRO: Falha ao gerar o PDF da tabela!")
    raise dash.exceptions.PreventUpdate