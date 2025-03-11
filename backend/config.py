import os

DATABASE_CONFIG = {
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASS", "root"),
    "database": os.getenv("DB_NAME", "uab_dashboard"),
    "charset": "utf8mb4",
    "port": int(os.getenv("DB_PORT", 3306))
}

CSV_FILES = {
    "tabela_docentes": "dados/arquivos_csv/docentes.csv",
    "unidades_curriculares": "dados/arquivos_csv/unidades_curriculares.csv",
    "distribuicao_carga": "dados/arquivos_csv/distribuicao_carga.csv"
}


