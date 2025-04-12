import os
import json
from datetime import datetime
from collections import defaultdict, Counter

class ConsultaModel:
    def __init__(self):
        self.registos = []

    def registar_consulta(self, utilizador_id, utilizador_nome, comando, seccao=None):
        self.registos.append({
            "data": datetime.now().isoformat(),
            "utilizador_id": utilizador_id,
            "nome": utilizador_nome,
            "comando": comando,
            "secao": seccao
        })

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
            "utilizadores_unicos": len(set(r["utilizador_id"] for r in self.registos)),
            "comandos_populares": list(comandos.items()),
            "seccoes_populares": list(secoes.items()),
            "utilizadores_ativos": [(uid, nome, count) for (uid, nome), count in utilizadores.items()]
        }

    def exportar_json(self, caminho="estatisticas/estatisticas.json"):
        os.makedirs(os.path.dirname(caminho), exist_ok=True)
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(self.obter_estatisticas(), f, indent=4, ensure_ascii=False)

    def obter_historico_utilizador(self, utilizador_id):
        return [r for r in self.registos if r["utilizador_id"] == utilizador_id]
