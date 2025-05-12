# ============================================================
# consulta_model.py - Gestão de Registos e Estatísticas
# ============================================================
# Unidade Curricular:
# Laboratório de Desenvolvimento de _Software_
#
# Objetivo:
# Modelo responsável por gerir registos de utilização do bot:
# 🔹 Carregamento e armazenamento persistente de dados
# 🔹 Registo de comandos utilizados e secções consultadas
# 🔹 Cálculo e exportação de estatísticas
# 🔹 Histórico de interações por utilizador
# ============================================================

import os
import json
from datetime import datetime
from collections import Counter
from interfaces import IModel

class ConsultaModel(IModel):
    """
    Classe responsável por gerir registos de consultas e estatísticas.
    Implementa a interface IModel.
    """
    
    def __init__(self, caminho_registos="estatistica/registos/registos.json"):
        """
        Inicializa o modelo de consultas com um caminho para o ficheiro de registos.
        Carrega os dados existentes e o mapeamento de seções.
        """
        self.caminho_registos = caminho_registos
        self.registos = self.carregar_dados()
        self.mapa_seccoes = self.carregar_seccoes("dados/puc/seccoes.txt")

    def carregar_dados(self):
        """
        Implementação do método da interface para carregar dados.
        Retorna os registos existentes.
        """
        return self.carregar_registos()

    def guardar_dados(self):
        """
        Implementação do método da _interface para guardar dados.
        Guarda os registos no ficheiro definido.
        """
        self.guardar_registos()

    @staticmethod
    def carregar_seccoes(caminho: str) -> dict:
        """
        Carrega o mapeamento de secções a partir de um ficheiro TXT.
        
        """
        mapa = {}
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                for linha in f:
                    linha = linha.strip()
                    if linha and "=" in linha:
                        chave, valor = linha.split("=", 1)
                        mapa[chave.strip()] = valor.strip()
        except FileNotFoundError:
            print(f"Ficheiro de secções não encontrado: {caminho}")
        return mapa
    
    def carregar_registos(self):
        """
        Carrega os registos a partir do ficheiro JSON.
        
        """
        if os.path.exists(self.caminho_registos):
            try:
                with open(self.caminho_registos, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"Erro ao carregar o ficheiro {self.caminho_registos}. O ficheiro pode estar corrompido.")
                return []
        return []

    def guardar_registos(self):
        """
        Guarda os registos no ficheiro JSON.
        """
        os.makedirs(os.path.dirname(self.caminho_registos), exist_ok=True)
        with open(self.caminho_registos, "w", encoding="utf-8") as f:
            json.dump(self.registos, f, indent=4, ensure_ascii=False)

    def registar_consulta(self, utilizador_id, nome, comando, seccao):
        """
        Regista uma nova consulta no sistema.
        
        """
        consulta = {
            "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "utilizador_id": utilizador_id,
            "nome": nome,
            "comando": comando,
            "secao": self.mapa_seccoes.get(seccao, seccao)
        }
        self.registos.append(consulta)
        self.guardar_registos()
        self.exportar_json()

    def obter_estatisticas(self):
        """
        Obtém estatísticas de uso do sistema.
        
        """
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
        """
        Exporta as estatísticas para um ficheiro JSON.
        
        """
        if not caminho:
            data_hoje = datetime.now().strftime("%Y%m%d")
            caminho = f"estatistica/estatisticas/estatisticas_{data_hoje}.json"

        os.makedirs(os.path.dirname(caminho), exist_ok=True)
        with open(caminho, "w", encoding="utf-8") as f:
            estatisticas = self.obter_estatisticas()
            print(f"Estatísticas a serem exportadas: {estatisticas}")
            json.dump(estatisticas, f, indent=4, ensure_ascii=False)
        print(f"✅ Estatísticas exportadas para: {caminho}")

    def obter_historico_utilizador(self, utilizador_id):
        """
        Retorna o histórico de consultas feitas por um utilizador específico.
        
        """
        return [consulta for consulta in self.registos if consulta["utilizador_id"] == utilizador_id]

