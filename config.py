import os

DATABASE_CONFIG = {
    "host": os.getenv("DB_HOST", "mysql.openapps.pt"),
    "user": os.getenv("DB_USER", "duarte"),
    "password": os.getenv("DB_PASS", "duarte01"),
    "database": os.getenv("DB_NAME", "uab"),
    "charset": "utf8mb4",
    "port": int(os.getenv("DB_PORT", 30306))
}

# Caminhos para os arquivos CSV no projeto
CSV_FILES = {
    # 🔹 Tabelas para análise do dashboard
    "comandos_pesquisados": "dados/arquivos_csv/comandos_pesquisados.csv",
    "comandos_sem_resposta": "dados/arquivos_csv/comandos_sem_resposta.csv",
    "frequencia_comandos_categoria": "dados/arquivos_csv/frequencia_comandos_categoria.csv",

    # 🔹 Novas tabelas para respostas do chatbot
    "respostas_comandos": "dados/arquivos_csv/respostas_comandos.csv",
    "perguntas_respostas": "dados/arquivos_csv/perguntas_respostas.csv"
}



