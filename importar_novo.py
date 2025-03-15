import sys
import os

# Caminho relativo ao diretório atual do ficheiro importar_novo.py
sys.path.append(os.path.abspath("../../"))

import dash
from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
from backend.conexao_mysql import obter_conexao_mysql

dash.register_page(__name__, path='/importar_novo', name="Importar Novo Comando")

layout = html.Div([
    html.H2("➕ Inserir novo comando e resposta"),
    html.Br(),

    html.Div([
        html.Label("Pergunta"),
        dcc.Input(id="input-pergunta", type="text", placeholder="Insira a pergunta", className="form-control"),
    ], className="mb-3"),

    html.Div([
        html.Label("Resposta"),
        dcc.Textarea(id="input-resposta", placeholder="Insira a resposta", style={"width": "100%", "height": 120}),
    ]),

    html.Button("Inserir", id="btn-inserir", className="btn btn-success", style={'marginTop': '20px'}),

    html.Div(id="output-msg", style={'marginTop': '20px'}),
])

@dash.callback(
    Output("output-msg", "children"),
    Input("btn-inserir", "n_clicks"),
    State("input-pergunta", "value"),
    State("input-resposta", "value")
)
def inserir_comando(n_clicks, pergunta, resposta):
    if not n_clicks:
        return ""

    if not pergunta or not resposta:
        return "⚠️ Pergunta e resposta são obrigatórias."

    conexao = obter_conexao_mysql()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            INSERT INTO comandos_pesquisados (comando, categoria, num_pesquisas, ultima_pesquisa)
            VALUES (%s, 'Outros', 1, NOW())
        """, (pergunta,))
        id_comando = cursor.lastrowid

        cursor.execute("""
            INSERT INTO respostas_comandos (id_comando, resposta, data_cadastro)
            VALUES (%s, %s, NOW())
        """, (id_comando, resposta))
        conexao.commit()

        return "✅ Comando e resposta inseridos com sucesso!"

    except pymysql.err.IntegrityError:
        conexao.rollback()
        return "⚠️ Este comando já existe na base de dados."

    except Exception as e:
        conexao.rollback()
        return f"🚨 Ocorreu um erro: {str(e)}"

    finally:
        cursor.close()
        conexao.close()
