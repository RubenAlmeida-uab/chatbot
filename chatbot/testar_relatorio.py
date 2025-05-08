import unittest
import os
import asyncio
from model.dados_model import DadosModel
from model.consulta_model import ConsultaModel
from utils.relatorio_exportador import (
    gerar_relatorio_md,
    gerar_pdf_a_partir_md,
    gerar_nomes_ficheiros
)
from controller.bot_controller import BotController


class TestBotFunctionality(unittest.TestCase):

    # ==========================================
    # Inicialização dos Modelos e Controladores
    # ==========================================

    def setUp(self):

        self.consulta_model = ConsultaModel()
        self.dados_model = DadosModel()
        self.bot_controller = BotController()

    # ===============================
    # Teste completo de integração
    # ===============================
    def testar_fluxo_completo(self):
        resposta = asyncio.run(
            self.bot_controller.processar_comando_admin("admin123", "Admin", "ajuda")
        )
        self.assertIn("Comandos disponíveis", resposta)

        # Registar consulta e verificar secções
        self.consulta_model.registar_consulta("1", "João", "ajuda", "ajuda")
        secoes = self.dados_model.obter_todas_seccoes()
        self.assertIn("competencias", secoes)

        # Verificar estatísticas atualizadas
        estatisticas = self.consulta_model.obter_estatisticas()
        self.assertGreater(estatisticas['total_consultas'], 0)

        # Gerar e verificar ficheiros de relatório
        json_path, md_path, pdf_path = gerar_nomes_ficheiros(base_dir="estatistica/testes")
        self.consulta_model.exportar_json(json_path)
        gerar_relatorio_md(json_path, md_path)
        gerar_pdf_a_partir_md(md_path, pdf_path)

        self.assertTrue(os.path.exists(md_path))
        self.assertTrue(os.path.exists(pdf_path))

    # ===============================
    # Teste de leitura de secções
    # ===============================
    def testar_leitura_secoes(self):
        secao = "competencias"
        dados = self.dados_model.obter_seccao(secao)
        self.assertIsNotNone(dados)
        self.assertIn("Competências", dados)

    # ===============================
    # Teste de registo de consultas
    # ===============================
    def testar_registrar_consultas(self):
        estatisticas_antes = self.consulta_model.obter_estatisticas()
        total_antes = estatisticas_antes['total_consultas']

        self.consulta_model.registar_consulta("1", "João", "ajuda", "competencias")

        estatisticas_depois = self.consulta_model.obter_estatisticas()
        total_depois = estatisticas_depois['total_consultas']

        self.assertEqual(total_depois, total_antes + 1)

        comandos = [comando[0] for comando in estatisticas_depois['comandos_populares']]
        self.assertIn("ajuda", comandos)

    # ===============================
    # Teste de geração de Markdown
    # ===============================
    def testar_gerar_relatorio_markdown(self):
        json_path, md_path, _ = gerar_nomes_ficheiros(base_dir="estatistica/testes")
        self.consulta_model.exportar_json(json_path)
        gerar_relatorio_md(json_path, md_path)
        self.assertTrue(os.path.exists(md_path))
        with open(md_path, 'r', encoding='utf-8') as f:
            conteudo = f.read()
            self.assertIn("Relatório de Utilização do Bot", conteudo)

    # ===============================
    # Teste de geração de PDF
    # ===============================
    def testar_gerar_pdf_a_partir_md(self):
        json_path, md_path, pdf_path = gerar_nomes_ficheiros(base_dir="estatistica/testes")
        self.consulta_model.exportar_json(json_path)
        gerar_relatorio_md(json_path, md_path)
        gerar_pdf_a_partir_md(md_path, pdf_path)
        self.assertTrue(os.path.exists(pdf_path))


if __name__ == "__main__":
    unittest.main()
