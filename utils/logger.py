import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime


class BotLogger:
    """
    Classe responsável por gerenciar os logs do chatbot.
    Centraliza todas as operações de logging em um único lugar.
    """

    def __init__(self):
        # Criar diretório de logs se não existir
        self.logs_dir = "logs"
        os.makedirs(self.logs_dir, exist_ok=True)

        # Configurar o logger
        self.logger = logging.getLogger('ChatbotLogger')
        self.logger.setLevel(logging.DEBUG)

        # Criar arquivo de log com data
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

    def info(self, message: str):
        """Log uma mensagem de nível INFO"""
        self.logger.info(message)

    def error(self, message: str):
        """Log uma mensagem de nível ERROR"""
        self.logger.error(message)

    def debug(self, message: str):
        """Log uma mensagem de nível DEBUG"""
        self.logger.debug(message)

    def warning(self, message: str):
        """Log uma mensagem de nível WARNING"""
        self.logger.warning(message)

    def critical(self, message: str):
        """Log uma mensagem de nível CRITICAL"""
        self.logger.critical(message)


# Criar uma instância global do logger
bot_logger = BotLogger()