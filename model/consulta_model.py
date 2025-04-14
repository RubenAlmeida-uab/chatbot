import os
import json
from datetime import datetime
from collections import Counter

class ConsultaModel:
    def __init__(self, caminho_registos="estatistica/registos/registos.json"):
        self.caminho_registos = caminho_registos
        self.registos = self.carregar_registos()

    def carregar_registos(self):
        if os.path.exists(self.caminho_registos):
            with open(self.caminho_registos, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def guardar_registos(self):
        os.makedirs(os.path.dirname(self.caminho_registos), exist_ok=True)
        with open(self.caminho_registos, "w", encoding="utf-8") as f:
            json.dump(self.registos, f, indent=4, ensure_ascii=False)

    def registar_consulta(self, utilizador_id, nome, comando, seccao):
        consulta = {
            "data": datetime.now().isoformat(),
            "utilizador_id": utilizador_id,
            "nome": nome,
            "comando": comando,
            "secao": seccao
        }
        self.registos.append(consulta)
        self.guardar_registos()
        self.exportar_json()

    def obter_estatisticas(self):
        total = len(self.registos)
        comandos = Counter(r['comando'] for r in self.registos)
        secoes = Counter(r['secao'] for r in self.registos if r['secao'])
        utilizadores = Counter((r['utilizador_id'], r['nome']) for r in self.registos)
        datas = [r['data'] for r in self.registos]

        return {
            "primeiro_acesso": min(datas) if datas else "",
            "ultimo_acesso": max(datas) if datas else "",
            "total_consultas": total,
            "utilizadores_unicos": len(utilizadores),
            "comandos_populares": list(comandos.items()),
            "seccoes_populares": list(secoes.items()),
            "utilizadores_ativos": [(uid, nome, count) for (uid, nome), count in utilizadores.items()]
        }

    def exportar_json(self, caminho=None):
        if not caminho:
            data_hoje = datetime.now().strftime("%Y%m%d")
            caminho = f"estatistica/relatorios/estatisticas_{data_hoje}.json"

        os.makedirs(os.path.dirname(caminho), exist_ok=True)
        with open(caminho, "w", encoding="utf-8") as f:
            estatisticas = self.obter_estatisticas()
            print(f"Estatísticas a serem exportadas: {estatisticas}")
            json.dump(estatisticas, f, indent=4, ensure_ascii=False)
        print(f"✅ Estatísticas exportadas para: {caminho}")


if __name__ == "__main__":
    consulta_model = ConsultaModel()
    consulta_model.registar_consulta("1", "João", "ajuda", "competencias")
    estatisticas = consulta_model.obter_estatisticas()
    print(estatisticas)

