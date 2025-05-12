# ============================================================
# logger.py - Sistema de Logging do Chatbot
# ============================================================
# Unidade Curricular:
# Laboratório de Desenvolvimento de _Software_
#
# Objetivo:
# Este módulo define uma classe centralizada para gestão de _logs:
# 🔹 Geração automática de ficheiros de _log com data
# 🔹 Rotação de ficheiros (5 MB por ficheiro, até 5 _backups)
# 🔹 Saída simultânea no terminal e ficheiro
# 🔹 Diferentes níveis de severidade (INFO, DEBUG, WARNING, ERROR, CRITICAL)
#
# Particularidade:
# Mensagens com estilo humorístico/pedagógico para facilitar _debugging
#
# Utilização:
# Importar `_bot_logger_` para usar em qualquer parte do bot.
# ============================================================

import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime


class BotLogger:
    """
    Classe responsável por gerir os:_logs do chatbot.
    Centraliza todas as operações de logging num único lugar.
    """
    def __init__(self):
        # Criar diretório de _logs se não existir
        self.logs_dir = "logs"
        os.makedirs(self.logs_dir, exist_ok=True)
        
        # Configurar o logger
        self.logger = logging.getLogger('ChatbotLogger')
        self.logger.setLevel(logging.DEBUG)
        
        # Limpar handlers existentes para evitar duplicação
        if self.logger.handlers:
            self.logger.handlers.clear()
            
        # Criar arquivo de _log com data
        log_file = os.path.join(self.logs_dir, f'chatbot_{datetime.now().strftime("%Y%m%d")}.log')
        
        # Configurar handler para arquivo
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=5 * 1024 * 1024,  # 5MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        
        # Configurar handler para console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Criar formatador
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Adicionar handlers ao logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def info(self, message: str, modulo: str = None):
        """
        _Log uma mensagem de nível INFO.
        """
        prefixo = f"[{modulo}] " if modulo else ""
        self.logger.info(f"Cheguei!! {prefixo}{message}")
    
    def error(self, message: str, modulo: str = None):
        """
        _Log uma mensagem de nível ERROR.
        """
        prefixo = f"[{modulo}] " if modulo else ""
        self.logger.error(f"Nop, não estou bem dá me uns minutos: {prefixo}{message}")
    
    def debug(self, message: str, modulo: str = None):
        """
        _Log uma mensagem de nível DEBUG.
        """
        prefixo = f"[{modulo}] " if modulo else ""
        self.logger.debug(f"A inspecionar o que não está bem: {prefixo}{message}")
    
    def warning(self, message: str, modulo: str = None):
        """
        _Log uma mensagem de nível WARNING.
        """
        prefixo = f"[{modulo}] " if modulo else ""
        self.logger.warning(f"Cautela, amigo...: {prefixo}{message}")
    
    def critical(self, message: str, modulo: str = None):
        """
        _Log uma mensagem de nível CRITICAL.
        """
        prefixo = f"[{modulo}] " if modulo else ""
        self.logger.critical(f"Ah, matáaaram-me. {prefixo}{message}")


bot_logger = BotLogger()
