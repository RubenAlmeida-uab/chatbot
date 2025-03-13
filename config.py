import os

DATABASE_CONFIG = {
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASS", "root"),
    "database": os.getenv("DB_NAME", "uab_dashboard"),
    "charset": "utf8mb4",
    "port": int(os.getenv("DB_PORT", 3306))
}

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))

CSV_FILES = {
    "tabela_docentes": os.path.join(BASE_DIR, "dados", "arquivos_csv", "docentes.csv"),
    "unidades_curriculares": os.path.join(BASE_DIR, "dados", "arquivos_csv", "unidades_curriculares.csv"),
    "distribuicao_carga": os.path.join(BASE_DIR, "dados", "arquivos_csv", "distribuicao_carga.csv")
}


