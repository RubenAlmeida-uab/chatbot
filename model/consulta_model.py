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
from utils.logger import bot_logger

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
        self.caminho_registos_admin = "estatistica/registos/registos_admin.json"
        self.registos_admin = self.carregar_registos_admin()
        self.logger = bot_logger

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
        print(f"Carregando seções do ficheiro: {caminho}")
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
    
    def carregar_registos_admin(self):
        if os.path.exists(self.caminho_registos_admin):
            try:
                with open(self.caminho_registos_admin, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print("Erro ao carregar registos_admin")
        return []

    def guardar_registos_admin(self):
        os.makedirs(os.path.dirname(self.caminho_registos_admin), exist_ok=True)
        with open(self.caminho_registos_admin, "w", encoding="utf-8") as f:
            json.dump(self.registos_admin, f, indent=4, ensure_ascii=False)

    def guardar_registos(self):
        """
        Guarda os registos no ficheiro JSON.
        """
        os.makedirs(os.path.dirname(self.caminho_registos), exist_ok=True)
        with open(self.caminho_registos, "w", encoding="utf-8") as f:
            json.dump(self.registos, f, indent=4, ensure_ascii=False)

    def registar_consulta(self, utilizador_id, nome, comando):
        """
        Regista uma nova consulta no sistema.
        
        """
        seccao = self.mapa_seccoes.get(comando, comando)


        consulta = {
            "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "utilizador_id": utilizador_id,
            "nome": nome,
            "comando": comando,
            "secao": seccao
        }
        self.registos.append(consulta)
        self.guardar_registos()
        self.exportar_json()
    
    def registar_consulta_admin(self, admin_id, comando, nome):
        """
        Regista uma nova consulta admin no sistema.
        
        """
        consulta = {
            "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "admin_id": admin_id,
            "nome": nome,
            "comando": comando
        }

        self.logger.info(f"Registando consulta admin: {consulta}")
        self.registos_admin.append(consulta)
        self.guardar_registos_admin()
        self.exportar_json_admin()


    def obter_estatisticas(self):
        """
        Obtém estatísticas de uso do sistema a partir do ficheiro JSON atualizado.
        """
        try:
            with open(self.caminho_registos, "r", encoding="utf-8") as f:
                dados = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {
                "primeiro_acesso": "",
                "ultimo_acesso": "",
                "total_consultas": 0,
                "utilizadores_unicos": 0,
                "comandos_populares": [],
                "seccoes_populares": [],
                "utilizadores_ativos": []
            }

        return {
            "primeiro_acesso": min(r['data'] for r in dados if 'data' in r) if dados else "",
            "ultimo_acesso": max(r['data'] for r in dados if 'data' in r) if dados else "",
            "total_consultas": len(dados),
            "utilizadores_unicos": len(Counter((r['utilizador_id'], r['nome']) for r in dados)),
            "comandos_populares": list(Counter(r['comando'] for r in dados).items()),
            "seccoes_populares": list(Counter(r['secao'] for r in dados if r.get('secao')).items()),
            "utilizadores_ativos": [
                (uid, nome, count)
                for (uid, nome), count in Counter((r['utilizador_id'], r['nome']) for r in dados).items()
            ]
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
    
    def exportar_json_admin(self, caminho=None):
        if not caminho:
            data_hoje = datetime.now().strftime("%Y%m%d")
            caminho = f"estatistica/estatisticas/estatisticas_admin_{data_hoje}.json"

        os.makedirs(os.path.dirname(caminho), exist_ok=True)
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(self.registos_admin, f, indent=4, ensure_ascii=False)
        print(f"✅ Estatísticas admin exportadas para: {caminho}")

    def obter_historico_utilizador(self, utilizador_id):
        """
        Retorna o histórico de consultas feitas por um utilizador específico.
        Lê diretamente do ficheiro JSON para garantir dados atualizados.
        """
        utilizador_id = str(utilizador_id)
        try:
            with open(self.caminho_registos, "r", encoding="utf-8") as f:
                return [
                    consulta for consulta in json.load(f)
                    if str(consulta.get("utilizador_id", "")) == utilizador_id
                ]
        except (FileNotFoundError, json.JSONDecodeError):
            return []