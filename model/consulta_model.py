import os
import json
from datetime import datetime
from collections import Counter

class ConsultaModel:
    def __init__(self, caminho="estatistica/estatisticas.json"):
        self.caminho = caminho
        self.registos = []
        self.primeiro_acesso = ""
        self.ultimo_acesso = ""
        self.carregar_json()

    def carregar_json(self):
        if os.path.exists(self.caminho):
            with open(self.caminho, "r", encoding="utf-8") as f:
                dados = json.load(f)
                self.primeiro_acesso = dados.get("primeiro_acesso", "")
                self.ultimo_acesso = dados.get("ultimo_acesso", "")
                # Nota: Aqui estamos apenas a carregar as datas. Deve carregar também registos se necessário.

    def registar_consulta(self, utilizador_id, nome, comando, seccao):
        consulta = {
            "data": datetime.now().isoformat(),
            "utilizador_id": utilizador_id,
            "nome": nome,
            "comando": comando,
            "secao": seccao
        }
        self.registos.append(consulta)

        if not self.primeiro_acesso:
            self.primeiro_acesso = consulta["data"]
        self.ultimo_acesso = consulta["data"]

        self.exportar_json()

    def obter_estatisticas(self):
        total = len(self.registos)
        comandos = Counter(r['comando'] for r in self.registos)
        secoes = Counter(r['secao'] for r in self.registos if r['secao'])
        utilizadores = Counter((r['utilizador_id'], r['nome']) for r in self.registos)

        return {
            "primeiro_acesso": self.primeiro_acesso,
            "ultimo_acesso": self.ultimo_acesso,
            "total_consultas": total,
            "utilizadores_unicos": len(utilizadores),
            "comandos_populares": list(comandos.items()),
            "seccoes_populares": list(secoes.items()),
            "utilizadores_ativos": [(uid, nome, count) for (uid, nome), count in utilizadores.items()]
        }

    def exportar_json(self, caminho="estatistica/estatisticas.json"):
        os.makedirs(os.path.dirname(caminho), exist_ok=True)
        with open(caminho, "w", encoding="utf-8") as f:
            estatisticas = self.obter_estatisticas()
            json.dump(estatisticas, f, indent=4, ensure_ascii=False)
        print(f"✅ Estatísticas exportadas para: {caminho}")

if __name__ == "__main__":
    consulta_model = ConsultaModel()
    consulta_model.registar_consulta("1", "João", "ajuda", "competencias")
    estatisticas = consulta_model.obter_estatisticas()
    print(estatisticas)

