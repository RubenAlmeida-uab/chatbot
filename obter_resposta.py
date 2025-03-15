import pymysql.cursors
from backend.conexao_mysql import obter_conexao_mysql


def buscar_resposta(comando):
    conexao = obter_conexao_mysql()
    cursor = conexao.cursor(pymysql.cursors.DictCursor)

    try:
        cursor.execute("SELECT id_comando FROM comandos_pesquisados WHERE comando = %s", (comando,))
        resultado = cursor.fetchone()

        if not resultado:
            cursor.execute("""
                INSERT INTO comandos_sem_resposta 
                (pergunta, categoria, num_tentativas, ultima_tentativa, status_resposta)
                VALUES (%s, 'Outros', 1, NOW(), 'Pendente')
                ON DUPLICATE KEY UPDATE num_tentativas = num_tentativas + 1, ultima_tentativa = NOW()
            """, (comando,))
            conexao.commit()
            return {"erro": "Ainda não há resposta cadastrada para esse comando."}

        id_comando = resultado['id_comando']

        # Aqui, INCREMENTA num_pesquisas pois o comando EXISTE e foi pesquisado novamente
        cursor.execute("""
            UPDATE comandos_pesquisados 
            SET num_pesquisas = num_pesquisas + 1, ultima_pesquisa = NOW() 
            WHERE id_comando = %s
        """, (id_comando,))
        conexao.commit()

        # Depois busca a resposta
        cursor.execute("SELECT resposta FROM respostas_comandos WHERE id_comando = %s", (id_comando,))
        resposta = cursor.fetchone()

        if resposta:
            return {"comando": comando, "resposta": resposta['resposta']}

        # Se o comando existe mas NÃO tem resposta
        cursor.execute("""
            INSERT INTO comandos_sem_resposta (pergunta, categoria, num_tentativas, ultima_tentativa, status_resposta, id_comando)
            VALUES (%s, 'Outros', 1, NOW(), 'Pendente', %s)
            ON DUPLICATE KEY UPDATE num_tentativas = num_tentativas + 1, ultima_tentativa = NOW()
        """, (comando, id_comando))
        conexao.commit()

        return {"erro": "Ainda não há resposta cadastrada para esse comando."}

    except Exception as e:
        return {"erro": str(e)}

    finally:
        cursor.close()
        conexao.close()


