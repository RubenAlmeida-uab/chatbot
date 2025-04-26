import os
from dotenv import load_dotenv
from utils.logger import bot_logger

class AdminChecker:
    _instance = None
    _admin_ids = set()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AdminChecker, cls).__new__(cls)
            cls._instance._load_admin_ids()
        return cls._instance

    def _load_admin_ids(self):
        """Carrega os IDs de admin do arquivo .env"""
        try:
            load_dotenv()
            admin_ids_str = os.getenv('ADMIN_IDS', '')
            if admin_ids_str:
                self._admin_ids = set(map(str.strip, admin_ids_str.split(',')))
                bot_logger.info(f"IDs de administradores carregados: {len(self._admin_ids)} admins")
            else:
                bot_logger.warning("Nenhum ID de administrador configurado no .env")
        except Exception as e:
            bot_logger.error(f"Erro ao carregar IDs de administradores: {str(e)}")
            self._admin_ids = set()

    def is_admin(self, user_id: str) -> bool:
        """Verifica se um usuário é admin pelo ID"""
        return str(user_id) in self._admin_ids