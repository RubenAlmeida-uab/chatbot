import unittest
import os
import asyncio  # <-- Adiciona esta importação
from model.mock_models import MockDadosModel as DadosModel
from model.consulta_model import ConsultaModel
from utils.relatorio_exportador import gerar_relatorio_md, gerar_pdf_a_partir_md
from controller.bot_controller import BotController


class TestBotFunctionality(unittest.TestCase):

    def setUp(self):
        self.consulta_model = ConsultaModel()
        self.dados_model = DadosModel()
        self.bot_controller = BotController()

    def test_fluxo_completo(self):
        resposta = asyncio.run(
            self.bot_controller.processar_comando_admin("admin123", "Admin", "ajuda")
        )
        self.assertIn("Comandos disponíveis", resposta)

        self.consulta_model.registar_consulta("1", "João", "ajuda", "ajuda")
        secoes = self.dados_model.obter_todas_seccoes()
        self.assertIn("competencias", secoes)

        estatisticas = self.consulta_model.obter_estatisticas()
        self.assertGreater(estatisticas['total_consultas'], 0)

        json_path = "estatistica/estatisticas.json"
        md_path = "estatistica/relatorio.md"
        pdf_path = "estatistica/relatorio.pdf"

        self.consulta_model.exportar_json(json_path)
        gerar_relatorio_md(json_path, md_path)
        gerar_pdf_a_partir_md(md_path, pdf_path)

        self.assertTrue(os.path.exists(md_path))
        self.assertTrue(os.path.exists(pdf_path))

    def test_leitura_secoes(self):
        secao = "competencias"
        dados = self.dados_model.obter_seccao(secao)
        self.assertIsNotNone(dados)
        self.assertIn("Competências", dados)

    def test_registrar_consultas(self):
        self.consulta_model.registar_consulta("1", "João", "ajuda", "competencias")
        estatisticas = self.consulta_model.obter_estatisticas()
        print(estatisticas)
        self.assertEqual(estatisticas['total_consultas'], 1)
        self.assertIn("ajuda", [comando[0] for comando in estatisticas['comandos_populares']])

    def test_gerar_relatorio_markdown(self):
        json_path = "estatistica/estatisticas.json"
        md_path = "estatistica/relatorio.md"
        self.consulta_model.exportar_json(json_path)
        gerar_relatorio_md(json_path, md_path)
        self.assertTrue(os.path.exists(md_path))
        with open(md_path, 'r', encoding='utf-8') as f:
            conteudo = f.read()
            self.assertIn("Relatório de Utilização do Bot", conteudo)

    def test_gerar_pdf_a_partir_md(self):
        md_path = "estatistica/relatorio.md"
        pdf_path = "estatistica/relatorio.pdf"
        gerar_pdf_a_partir_md(md_path, pdf_path)
        self.assertTrue(os.path.exists(pdf_path))


if __name__ == "__main__":
    unittest.main()
