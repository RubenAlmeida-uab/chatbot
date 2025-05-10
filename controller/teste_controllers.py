# ========================================================================
# teste_controllers.py - Testes Simples dos Controladores do Chatbot
# ========================================================================
# Unidade Curricular:
# Laboratório de Desenvolvimento de Software
#
# Objetivo:
# Este script realiza testes básicos (síncronos) sobre os controladores:
# 🔹 `UserController`: Testa comandos da unidade curricular e eventos.
# 🔹 `BotController`: Testa extração de estatísticas e histórico.
#
# Funcionalidades:
# - Simula chamadas de comandos como "ajuda", "listar_seccoes" e "puc"
# - Exibe saídas formatadas no terminal
# - Verifica a integração entre controladores e os modelos
#
# Notas:
# - Não usa chamadas assíncronas para facilitar testes manuais
# - Pode ser executado diretamente pela linha de comando
# ========================================================================

import os
import sys
from user_controller import UserController
from bot_controller import BotController

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main():
    """Função principal para testar os controllers"""
    print("=== Testes dos Controllers ===")
    
    # ----- Testar UserController -----
    print("\nTestar UserController...")
    user_controller = UserController()
    
    # Regista callback  para demonstrar eventos
    def ao_processar_comando(utilizador_id, utilizador_nome, comando, seccao, sucesso):
        print(f"Evento: Comando '{comando}' processado com {'sucesso' if sucesso else 'falha'}")
    
    # Regista o callback
    user_controller.adicionar_listener_comando_processado(ao_processar_comando)
    
    # Testar alguns comandos
    print("\n1. Obter ajuda:")
    resposta = user_controller.obter_resposta("123456", "Utilizador1", "ajuda", None)
    print(f"Resposta recebida de {len(resposta)} caracteres")
    print(resposta[:200] + "..." if len(resposta) > 200 else resposta)
    
    print("\n2. Obter lista de secções:")
    resposta = user_controller.obter_resposta("123456", "Utilizador1", "listar_seccoes", None)
    print(resposta)
    
    print("\n3. Obter secção recursos:")
    resposta = user_controller.obter_resposta("123456", "Utilizador1", "puc", "recursos")
    print(resposta)
    
    # ----- Testar BotController (apenas métodos síncronos) -----
    print("\nTestar BotController (apenas métodos síncronos)...")
    bot_controller = BotController()
    
    def ao_aceder_estatisticas(admin_id, estatisticas):
        print(f"Evento: Estatísticas acedidas pelo admin '{admin_id}'")    
    
    bot_controller.adicionar_listener_estatisticas_acedidas(ao_aceder_estatisticas)
    
    # Testa obtenção de estatísticas
    print("\n1. Obter estatísticas")
    estatisticas = bot_controller.obter_estatisticas("admin123")
    print(f"Total de consultas: {estatisticas['total_consultas']}")
    print(f"Utilizadores únicos: {estatisticas['utilizadores_unicos']}")
    
    # Testar obtenção de histórico
    print("\n2. Obter histórico de utilizador:")
    historico = bot_controller.obter_utilizador_historico("123456", "admin123")
    if historico:
        print(f"Histórico obtido com {len(historico)} registos")
        for item in historico:
            print(f"- {item['data']}: {item['comando']}")
    else:
        print("Nenhum histórico encontrado")
    
    print("\n=== Teste concluído com sucesso! ===")


if __name__ == "__main__":
    main()