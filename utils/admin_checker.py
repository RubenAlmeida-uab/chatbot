# ============================================================
# admin_checker.py - Verificação de Administradores do Bot
# ============================================================
# Unidade Curricular:
# Laboratório de Desenvolvimento de _Software_
#
# Objetivo:
# Este módulo define um sistema de verificação de permissões administrativas:
# 🔹 Carrega os _IDs de administradores a partir do ficheiro `_.env_`
# 🔹 Implementa o padrão Singleton para garantir instância única
# 🔹 Fornece método `_administrador(user_id)_` para validação
# 🔹 Inclui decorador `_@env_admin_` para proteger comandos administrativos
#
# Notas:
# - Permite autenticação flexível sem hardcoding de permissões
# - Integra diretamente com o sistema de comandos do Discord
# ============================================================

import os
from dotenv import load_dotenv
from utils.logger import bot_logger
from discord.ext import commands


class AdminChecker:
    _instance = None
    _admin_ids = set()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AdminChecker, cls).__new__(cls)
            cls._instance._carregar_admin_ids()
        return cls._instance

    def _carregar_admin_ids(self):
        """Carrega os _IDs de admin do arquivo .env"""
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

    def administrador(self, user_id: str) -> bool:
        """Verifica se um usuario é admin pelo _ID"""

    def is_admin(self, user_id: str) -> bool:
        """Verifica se um utilizador é admin pelo ID"""

        return str(user_id) in self._admin_ids

# Decorador para usar nos comandos


def env_admin():
    def predicate(ctx):
        checker = AdminChecker()
        return checker.administrador(ctx.author.id)
    return commands.check(predicate)
