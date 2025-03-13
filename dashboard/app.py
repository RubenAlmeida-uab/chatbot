import os
import datetime
from fpdf import FPDF
import dash
from dash import dcc, html, page_container
import dash_bootstrap_components as dbc


app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

# Sidebar
sidebar = dbc.Nav(
    [
        html.Div([
            html.Img(src="/assets/logo.png", style={'width': '100%', 'padding': '10px'}),
            html.Hr(),
        ]),
        dbc.NavLink("Início", href="/home", active="exact"),
        dbc.NavLink("📊 Comandos Pesquisados", href="/comandos_pesquisados", active="exact"),
        dbc.NavLink("❓ Comandos sem Resposta", href="/comandos_sem_resposta", active="exact"),
        dbc.NavLink("📈 Frequência por Categoria", href="/frequencia_comandos_categoria", active="exact"),

        html.Div([
            html.Label("Fonte de Dados:"),
            dcc.Dropdown(
                id="dropdown_fonte_dados",
                options=[
                    {'label': 'MySQL', 'value': 'mysql'},
                    {'label': 'CSV', 'value': 'csv'}
                ],
                value='mysql',
                clearable=False,
                style={'margin-top': '10px'}
            )
        ], style={'padding': '10px'})
    ],
    vertical=True,
    pills=True,
    className="bg-light",
    style={"height": "100vh", "width": "250px"}
)

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(sidebar, width="auto"),
                dbc.Col(page_container, style={"padding": "20px"})
            ]
        )
    ],
    fluid=True,
    style={
        "backgroundImage": "url('/assets/background.jpg')",
        "backgroundSize": "cover"
    }
)


if __name__ == '__main__':
    app.run(debug=True, port=8050)


