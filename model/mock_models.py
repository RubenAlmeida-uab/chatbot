import json

class MockDadosModel:
    def __init__(self):
        # Define algumas seções de exemplo
        self.secoes = {
            "competencias": "Competências: Python, Java, C++",
            "projetos": "Projetos: Chatbot, API, WebApp"
        }

    def obter_todas_seccoes(self):
        # Retorna uma lista com as chaves das seções
        return list(self.secoes.keys())

    def obter_seccao(self, secao):
        # Retorna o conteúdo da seção ou uma mensagem se não existir
        return self.secoes.get(secao, "Seção não encontrada")


class MockConsultaModel:
    def __init__(self):
        # Lista para registar consultas feitas
        self.consultas = []

    def registar_consulta(self, id, nome, comando, secao):
        # Simula o registro de uma consulta, armazenando o comando e a seção solicitada
        self.consultas.append((comando, secao))

    def obter_estatisticas(self):
        # Calcula o total de consultas e agrupa quantas vezes cada comando aparece
        total = len(self.consultas)
        comandos_populares = {}
        for comando, secao in self.consultas:
            comandos_populares[comando] = comandos_populares.get(comando, 0) + 1

        # Convertendo o dicionário para uma lista de tuplas para manter um formato similar
        comandos_populares = list(comandos_populares.items())
        return {"total_consultas": total, "comandos_populares": comandos_populares}

    def exportar_json(self, path):
        # Exporta as estatísticas para um ficheiro JSON
        stats = self.obter_estatisticas()
        with open(path, "w", encoding="utf-8") as f:
            json.dump(stats, f, indent=4)

