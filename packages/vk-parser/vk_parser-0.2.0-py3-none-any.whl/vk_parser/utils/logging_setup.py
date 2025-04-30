"""
Настройка логирования для приложения.
"""
import logging
import os
import sys
from typing import Optional
from datetime import datetime
from pathlib import Path


def setup_logging(log_file: Optional[str] = None, level: int = logging.INFO, log_dir: str = "logs") -> str:
    """
    Настраивает логирование для приложения.
    
    Args:
        log_file: Путь к файлу логирования (если None, генерируется автоматически)
        level: Уровень логирования
        log_dir: Директория для логов
        
    Returns:
        str: Путь к файлу логов
    """
    logs_path = Path(log_dir)
    logs_path.mkdir(exist_ok=True, parents=True)
    
    if not log_file:
        today = datetime.now().strftime("%Y-%m-%d")
        log_file = logs_path / f"vk_parser_{today}.log"
    else:
        if not os.path.dirname(log_file):
            log_file = logs_path / log_file
    
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    # Устанавливаем форматирование с временем, модулем и уровнем
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    handlers = [
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(log_file, encoding='utf-8')
    ]
    
    logging.basicConfig(
        level=level,
        format=log_format,
        handlers=handlers
    )
    
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('vk_api').setLevel(logging.WARNING)
    
    try:
        from logging.handlers import RotatingFileHandler
        
        max_log_size = 10 * 1024 * 1024
        
        for i, handler in enumerate(logging.root.handlers):
            if isinstance(handler, logging.FileHandler) and not isinstance(handler, RotatingFileHandler):
                rotating_handler = RotatingFileHandler(
                    log_file, maxBytes=max_log_size, backupCount=5, encoding='utf-8'
                )
                rotating_handler.setFormatter(logging.Formatter(log_format))
                rotating_handler.setLevel(level)
                
                logging.root.handlers[i] = rotating_handler
    except ImportError:
        pass
    
    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized. Logs will be saved to {log_file}")
    
    return str(log_file)


def get_logger(name: str) -> logging.Logger:
    """
    Получает настроенный логгер для указанного модуля.
    
    Args:
        name: Имя модуля
        
    Returns:
        logging.Logger: Настроенный логгер
    """
    return logging.getLogger(name) 