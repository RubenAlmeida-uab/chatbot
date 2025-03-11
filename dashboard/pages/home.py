import dash
from dash import html

dash.register_page(__name__, path='/home')

layout = html.Div([
    html.H1("Dashboard Acadêmico", style={'textAlign': 'center'}),
    html.P("Selecione uma página na barra lateral para começar.", style={'textAlign': 'center'})
])
