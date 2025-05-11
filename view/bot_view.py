#módulo esta a implementar uma funcionalidade que pode ser implementada caso os administradores decidam gerar relatórios 
# em PDF com as estatísticas de uso do bot.Atualmente a geracão de relatórios em PDF não está implementada, mas a estrutura básica para isso está presente.
#

import os
from datetime import datetime
import discord
from weasyprint import HTML


class BotView:
    """
    Classe responsável pela apresentação dos dados.
    Gera relatórios em PDF e fornece métodos para formatação de respostas.
    """
    
    def __init__(self):
        """
        Inicializa a classe BotView.
        """
        pass

    def gerar_relatorio_pdf(self, estatisticas):
        """
        Gera um relatório em PDF com as estatísticas fornecidas.

        """
        # Cria o conteúdo do relatório em HTML
        html_content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                h1 {{ color: #2c3e50; }}
                h2 {{ color: #34495e; margin-top: 20px; }}
                .section {{ margin: 20px 0; }}
                .stat-item {{ margin: 10px 0; }}
                .highlight {{ color: #3498db; }}
            </style>
        </head>
        <body>
            <h1>Relatório de Uso do Bot LDS</h1>
            <p>Data de geração: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>

            <div class="section">
                <h2>Informações Gerais</h2>
                <div class="stat-item">Período: {estatisticas['primeiro_acesso']} até {estatisticas['ultimo_acesso']}</div>
                <div class="stat-item">Total de consultas: <span class="highlight">{estatisticas['total_consultas']}</span></div>
                <div class="stat-item">Utilizadores únicos: <span class="highlight">{estatisticas['utilizadores_unicos']}</span></div>
            </div>

            <div class="section">
                <h2>Comandos mais populares</h2>
                <ul>
        """

        # Adiciona os comandos mais populares
        for comando, contagem in estatisticas['comandos_populares']:
            html_content += f'        <li>{comando}: {contagem} consultas</li>\n'

        html_content += """
                </ul>
            </div>

            <div class="section">
                <h2>Secções mais consultadas</h2>
                <ul>
        """

        # Adiciona as secções mais consultadas
        for seccao, contagem in estatisticas['seccoes_populares']:
            html_content += f'        <li>{seccao}: {contagem} consultas</li>\n'

        html_content += """
                </ul>
            </div>

            <div class="section">
                <h2>Utilizadores mais ativos</h2>
                <ul>
        """

        # Adiciona os utilizadores mais ativos
        for utilizador_id, nome, contagem in estatisticas['utilizadores_ativos']:
            html_content += f'        <li>{nome} (ID: {utilizador_id}): {contagem} consultas</li>\n'

        html_content += """
                </ul>
            </div>
        </body>
        </html>
        """

        # Cria um ficheiro temporário com o relatório
        data_hora = datetime.now().strftime('%Y%m%d_%H%M%S')
        html_filename = f"estatistica/relatorios/temp_relatorio_{data_hora}.html"
        pdf_filename = f"estatistica/relatorios/relatorio_bot_lds_{data_hora}.pdf"

        # Garante que o diretório existe
        os.makedirs(os.path.dirname(pdf_filename), exist_ok=True)

        # Guarda o HTML temporário
        with open(html_filename, 'w', encoding='utf-8') as f:
            f.write(html_content)

        # Converte HTML para PDF usando weasyprint
        HTML(html_filename).write_pdf(pdf_filename)

        # Remove o ficheiro HTML temporário
        os.remove(html_filename)

        # Retorna o ficheiro para ser enviado pelo Discord
        return discord.File(pdf_filename)
