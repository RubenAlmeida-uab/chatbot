import json
import os
from collections import Counter
from datetime import datetime



class MockDadosModel:
    def __init__(self):
        # Inicializao atributo registos como uma lista vazia
        self.registos = []

    @staticmethod
    def obter_todas_seccoes():
        return ["competencias", "metodologia", "avaliacao", "ajuda"]

    @staticmethod
    def obter_seccao(nome):
        if nome == "competencias":
            return "Conteúdo da seção Competências"
        elif nome == "ajuda":
            return """
# 📚 Bot LDS - Comandos Disponíveis 📚

## Informações Gerais
`!puc` - Visão geral do Plano da Unidade Curricular
`!unidade_curricular` - Descrição detalhada da disciplina
`!listar_seccoes` - Lista todas as secções disponíveis para consulta

## Conteúdo Acadêmico
`!competencias` - Competências a desenvolver na disciplina
`!roteiro` - Roteiro completo do conteúdo a trabalhar
`!metodologia` - Métodos de trabalho e aprendizagem
            """
        return f"Conteúdo simulado da secção: {nome}"



    def registar_consulta(self, utilizador_id, nome, comando, seccao):
        # Regista a consulta simulada
        print(f"[Mock] Consulta registada: {comando} - {seccao}")
        self.registos.append({
            "data": datetime.now().isoformat(),
            "utilizador_id": utilizador_id,
            "nome": nome,
            "comando": comando,
            "secao": seccao
        })

    def obter_estatisticas(self):
        # Retorna as estatísticas simuladas
        total = len(self.registos)
        print(f"Total de registros: {total}")  # Verifica o total de registros
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
        # Exporta as estatísticas para um arquivo JSON
        os.makedirs(os.path.dirname(caminho), exist_ok=True)
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(self.obter_estatisticas(), f, indent=4, ensure_ascii=False)
        print(f"✅ Estatísticas exportadas para: {caminho}")

    def obter_historico_utilizador(self, utilizador_id):
        # Retorna o histórico de um utilizador específico
        return [r for r in self.registos if r["utilizador_id"] == utilizador_id]


class MockConsultaModel(MockDadosModel):
    def registar_consulta(self, utilizador_id, nome, comando, seccao):
        print(f"[Mock] Consulta registada: {comando} - {seccao}")
        self.registos.append({  # ← esta linha estava em falta!
            "data": datetime.now().isoformat(),
            "utilizador_id": utilizador_id,
            "nome": nome,
            "comando": comando,
            "secao": seccao
        })
