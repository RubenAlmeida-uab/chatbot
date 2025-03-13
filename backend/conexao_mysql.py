import pymysql
from config import DATABASE_CONFIG

def obter_conexao_mysql():
    return pymysql.connect(
        host=DATABASE_CONFIG["host"],
        user=DATABASE_CONFIG["user"],
        password=DATABASE_CONFIG["password"],
        db=DATABASE_CONFIG["database"],
        charset=DATABASE_CONFIG["charset"],
        port=DATABASE_CONFIG["port"],
        cursorclass=pymysql.cursors.DictCursor
    )

def obter_dados_mysql(tabela):
    conexao = obter_conexao_mysql()
    try:
        with conexao.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {tabela}")
            resultado = cursor.fetchall()
            return resultado
    except Exception as e:
        print(f"Erro ao acessar MySQL: {e}")
        return []
    finally:
        conexao.close()
