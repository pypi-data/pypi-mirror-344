"""
Модуль для работы с настройками парсера.
"""
from dataclasses import dataclass
from configparser import ConfigParser
from typing import Optional, List
import os
import logging

logger = logging.getLogger(__name__)

@dataclass
class VKConfig:
    """Конфигурация для парсера VK."""
    access_token: str
    start_user_id: Optional[str] = None
    max_depth: int = 5
    max_users: int = 20000
    batch_size: int = 25
    request_delay: float = 0.35
    save_interval: int = 5000
    load_communities: bool = False
    communities_ids: List[str] = None
    max_community_members: int = 10000


def load_config(config_path: str = "config.ini") -> VKConfig:
    """Загружает конфигурацию из INI файла.
    
    Args:
        config_path: Путь к файлу конфигурации
        
    Returns:
        VKConfig: Объект конфигурации
    """
    config = ConfigParser()
    
    if not os.path.exists(config_path):
        logger.error(f"Config file not found: {config_path}")
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config.read_file(f)
        
        logger.info(f"Config loaded from {config_path}")
        
        communities_str = config.get("collection", "communities_ids", fallback="")
        communities_ids = [comm_id.strip() for comm_id in communities_str.split(",") if comm_id.strip()] if communities_str else None
        
        return VKConfig(
            access_token=config["credentials"]["access_token"],
            start_user_id=config.get("credentials", "start_user_id", fallback="").strip() or None,
            max_depth=int(config.get("collection", "max_depth", fallback=5)),
            max_users=int(config.get("collection", "max_users", fallback=20000)),
            batch_size=int(config.get("collection", "batch_size", fallback=25)),
            request_delay=float(config.get("collection", "request_delay", fallback=0.35)),
            save_interval=int(config.get("collection", "save_interval", fallback=5000)),
            load_communities=config.getboolean("collection", "load_communities", fallback=False),
            communities_ids=communities_ids,
            max_community_members=int(config.get("collection", "max_community_members", fallback=10000))
        )
    except UnicodeDecodeError as e:
        logger.warning(f"Failed to read config with UTF-8 encoding, trying cp1251: {e}")
        try:
            with open(config_path, 'r', encoding='cp1251') as f:
                config.read_file(f)
            
            logger.info(f"Config loaded from {config_path} with cp1251 encoding")
            
            communities_str = config.get("collection", "communities_ids", fallback="")
            communities_ids = [comm_id.strip() for comm_id in communities_str.split(",") if comm_id.strip()] if communities_str else None
            
            return VKConfig(
                access_token=config["credentials"]["access_token"],
                start_user_id=config.get("credentials", "start_user_id", fallback="").strip() or None,
                max_depth=int(config.get("collection", "max_depth", fallback=5)),
                max_users=int(config.get("collection", "max_users", fallback=20000)),
                batch_size=int(config.get("collection", "batch_size", fallback=25)),
                request_delay=float(config.get("collection", "request_delay", fallback=0.35)),
                save_interval=int(config.get("collection", "save_interval", fallback=5000)),
                load_communities=config.getboolean("collection", "load_communities", fallback=False),
                communities_ids=communities_ids,
                max_community_members=int(config.get("collection", "max_community_members", fallback=10000))
            )
        except Exception as e2:
            logger.error(f"Failed to load config: {e2}")
            raise
    except Exception as e:
        logger.error(f"Error loading config: {e}")
        raise 