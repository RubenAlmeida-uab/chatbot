import pymysql
from backend.config import DATABASE_CONFIG


def obter_conexao_mysql():
    return pymysql.connect(
        host="mysql.openapps.pt",
        user="duarte",
        password="duarte01",
        db="uab",   # força explicitamente a BD correta
        charset="utf8mb4",
        port=30306,
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

if __name__ == '__main__':
    try:
        conexao = obter_conexao_mysql()
        print("✅ Conexão estabelecida com sucesso:", conexao)
        conexao.close()
    except Exception as e:
        print("❌ Erro na conexão:", e)

