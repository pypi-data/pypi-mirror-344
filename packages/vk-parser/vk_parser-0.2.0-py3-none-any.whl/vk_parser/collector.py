"""
Основной модуль сборщика данных из ВКонтакте.
"""
import logging
import asyncio
import signal
import time
from typing import List, Dict, Set, Any, Optional

from vk_parser.config.settings import VKConfig
from vk_parser.api.vk_client import VKClient
from vk_parser.utils.storage import DataStorage
from vk_parser.utils.state_manager import StateManager
from vk_parser.models.user import VKUser


logger = logging.getLogger(__name__)


class VKDataCollector:
    """Основной класс для сбора данных из ВКонтакте.
    
    Собирает информацию о пользователях, их постах и сообществах, в которых они состоят.
    Выполняет сбор данных с помощью асинхронных запросов к API ВКонтакте.
    Поддерживает возобновление сбора данных с точки остановки.
    """
    
    def __init__(self, config: VKConfig, resume: bool = False, state_file: str = "vk_parser_state.json"):
        """
        Инициализирует сборщик данных.
        
        Args:
            config: Конфигурация для сборщика
            resume: Флаг возобновления сбора данных
            state_file: Путь к файлу состояния
        """
        self.config = config
        self.api_client = VKClient(config.access_token, config.request_delay)
        self.storage = DataStorage()
        self.state_manager = StateManager(state_file)
        
        self.need_save_state = False
        self.last_state_save = time.time()
        self.state_save_interval = 10  # Сохраняем состояние каждые 10 секунд
        
        # Загружаем сохраненное состояние или инициализируем новое
        if resume and self.state_manager.has_saved_state():
            state = self.state_manager.load_state()
            self.used_users = state["used_users"]
            self.unique_users = state["unique_users"]
            self.batch_data = []  # Всегда начинаем с пустых данных
            self.batch_index = state["batch_index"]
            self.users_counter = state["users_counter"]
            self.in_progress_users = state.get("in_progress_users", [])
            self.last_user_id = state.get("last_user_id", None)  # Сохраняем last_user_id
            logger.info(f"Возобновление сбора с {self.users_counter} пользователей, пакет {self.batch_index}")
        else:
            self.used_users: Set[str] = set()
            self.unique_users: Set[str] = set()
            self.in_progress_users: List[str] = []
            self.last_user_id = None
            
            # Данные текущего пакета
            self.batch_data: List[Dict[str, Any]] = []
            self.batch_index: int = 1
            self.users_counter: int = 0
        
        self._setup_signal_handlers()
    
    def _setup_signal_handlers(self):
        """Настраивает обработчики сигналов для корректного завершения."""
        # Только для *nix систем
        try:
            signal.signal(signal.SIGINT, self._handle_exit)
            signal.signal(signal.SIGTERM, self._handle_exit)
        except (AttributeError, ValueError):
            # Windows не поддерживает SIGTERM
            pass
    
    def _handle_exit(self, signum, frame):
        """Обрабатывает сигналы завершения."""
        logger.info(f"Получен сигнал {signum}, сохраняем состояние и завершаем работу...")
        self.need_save_state = True
        raise KeyboardInterrupt
    
    def filter_friends(self, friends: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Фильтрует только открытые профили.
        
        Args:
            friends: Список профилей друзей
            
        Returns:
            List[Dict[str, Any]]: Отфильтрованный список профилей
        """
        return [f for f in friends if not f.get("is_closed", True)]
    
    def _save_current_state(self, last_user_id: Optional[str] = None):
        """
        Сохраняет текущее состояние сбора данных.
        
        Args:
            last_user_id: ID последнего обрабатываемого пользователя
        """
        # Сохраняем последний обработанный ID в экземпляре класса
        self.last_user_id = last_user_id
        
        self.state_manager.save_state(
            self.used_users,
            self.unique_users,
            last_user_id,
            self.batch_index,
            self.users_counter,
            self.in_progress_users
        )
    
    def _check_periodic_state_save(self):
        """Периодически сохраняет состояние, чтобы не потерять прогресс."""
        current_time = time.time()
        if current_time - self.last_state_save > self.state_save_interval:
            self._save_current_state()
            self.last_state_save = current_time
    
    async def collect_friends(self, user_id: str, depth: int = 1) -> None:
        """
        Асинхронно собирает информацию о друзьях, их постах и сообществах.
        
        Для каждого пользователя собирается:
        - Профиль с основной информацией
        - Последние посты со стены
        - Список сообществ, в которых состоит пользователь (если load_communities=True)
        
        Args:
            user_id: ID пользователя для начала сбора
            depth: Текущая глубина рекурсии
        """
        self._check_periodic_state_save()
        
        if (
            user_id in self.used_users
            or depth > self.config.max_depth
            or self.users_counter >= self.config.max_users
        ):
            return
        
        if user_id not in self.in_progress_users:
            self.in_progress_users.append(user_id)
        
        try:
            self.used_users.add(user_id)
            
            friends_ids = await self.api_client.get_friends_ids(user_id)
            logger.info(f"Пользователь {user_id} имеет {len(friends_ids)} друзей")
            
            friends_info = await self.api_client.get_users_info(friends_ids)
            filtered_friends = self.filter_friends(friends_info)
            logger.info(f"Открытых профилей: {len(filtered_friends)}")
            
            posts = await self.api_client.get_posts_batch([f["id"] for f in filtered_friends])
            
            communities = {}
            if self.config.load_communities:
                communities = await self.api_client.get_communities_batch([f["id"] for f in filtered_friends])
                logger.info(f"Загружены сообщества для {len(communities)} пользователей")
            
            for friend in filtered_friends:
                if friend["id"] in self.unique_users or self.users_counter >= self.config.max_users:
                    continue
                
                friend_posts = posts.get(friend["id"], [])
                if not friend_posts:
                    continue
                
                friend_communities = []
                if self.config.load_communities:
                    friend_communities = communities.get(friend["id"], [])
                
                friend_data = friend.copy()
                friend_data["posts"] = friend_posts
                friend_data["communities"] = friend_communities
                
                self.batch_data.append(friend_data)
                self.unique_users.add(friend["id"])
                self.users_counter += 1
                
                if self.users_counter % self.config.save_interval == 0:
                    self.storage.save_batch(self.batch_data, self.batch_index)
                    self.storage.cleanup_temp()
                    self.batch_data = []
                    self.batch_index += 1
                    
                    self._save_current_state(user_id)
                
                if self.users_counter >= self.config.max_users:
                    logger.info(f"Достигнут максимальный лимит пользователей: {self.users_counter}")
                    return
            
            if depth < self.config.max_depth and self.users_counter < self.config.max_users:
                tasks = []
                for friend in filtered_friends:
                    task = self.collect_friends(friend["id"], depth + 1)
                    tasks.append(task)
                await asyncio.gather(*tasks)
            
        except asyncio.CancelledError:
            logger.warning(f"Задача для пользователя {user_id} была отменена")
            raise
        except Exception as e:
            logger.error(f"Ошибка при обработке пользователя {user_id}: {e}")
        finally:
            if user_id in self.in_progress_users:
                self.in_progress_users.remove(user_id)
    
    async def collect_community_members(self, community_id: str) -> None:
        """
        Асинхронно собирает информацию о подписчиках сообщества.
        
        Args:
            community_id: ID сообщества ВКонтакте
        """
        self._check_periodic_state_save()
        
        try:
            logger.info(f"Сбор участников сообщества {community_id}")
            
            members_ids = await self.api_client.get_community_members(
                community_id, 
                max_members=self.config.max_community_members
            )
            
            logger.info(f"Сообщество {community_id} имеет {len(members_ids)} доступных участников")
            
            if not members_ids:
                logger.warning(f"Не найдено участников для сообщества {community_id}")
                return
            
            batch_size = self.config.batch_size
            for i in range(0, len(members_ids), batch_size):
                if self.users_counter >= self.config.max_users:
                    logger.info(f"Достигнут максимальный лимит пользователей: {self.users_counter}")
                    return
                
                batch_ids = members_ids[i:i+batch_size]
                
                filtered_ids = [uid for uid in batch_ids if uid not in self.unique_users]
                
                if not filtered_ids:
                    continue
                
                users_info = await self.api_client.get_users_info(filtered_ids)
                
                filtered_users = self.filter_friends(users_info)
                
                if not filtered_users:
                    continue
                
                posts = await self.api_client.get_posts_batch([u["id"] for u in filtered_users])
                
                communities = {}
                if self.config.load_communities:
                    communities = await self.api_client.get_communities_batch([u["id"] for u in filtered_users])
                
                for user in filtered_users:
                    if user["id"] in self.unique_users or self.users_counter >= self.config.max_users:
                        continue
                    
                    user_posts = posts.get(user["id"], [])
                    if not user_posts:
                        continue
                    
                    user_communities = []
                    if self.config.load_communities:
                        user_communities = communities.get(user["id"], [])
                    
                    user_data = user.copy()
                    user_data["posts"] = user_posts
                    user_data["communities"] = user_communities
                    user_data["source_community"] = community_id  # Добавляем источник
                    
                    self.batch_data.append(user_data)
                    self.unique_users.add(user["id"])
                    self.users_counter += 1
                    
                    if self.users_counter % self.config.save_interval == 0:
                        self.storage.save_batch(self.batch_data, self.batch_index)
                        self.storage.cleanup_temp()
                        self.batch_data = []
                        self.batch_index += 1
                        
                        # Сохраняем состояние с указанием текущего сообщества и индекса
                        self._save_current_state(f"community_{community_id}_{i}")
                
                logger.info(f"Обработано {min(i + batch_size, len(members_ids))}/{len(members_ids)} участников "
                           f"из сообщества {community_id}. Всего пользователей: {self.users_counter}")
                
                # Периодически сохраняем состояние после обработки каждого пакета участников
                self._save_current_state(f"community_{community_id}_{i}")
            
            logger.info(f"Завершен сбор участников для сообщества {community_id}")
            
        except asyncio.CancelledError:
            logger.warning(f"Задача для сообщества {community_id} была отменена")
            raise
        except Exception as e:
            logger.error(f"Ошибка при обработке сообщества {community_id}: {e}")
    
    async def run(self) -> None:
        """Запускает процесс сбора данных."""
        logger.info("Запуск сбора данных...")
        
        try:
            has_data_sources = False
            
            # Проверяем, есть ли сохраненное состояние с информацией о сообществах
            last_community_id = None
            if hasattr(self, 'last_user_id') and self.last_user_id:
                last_id = self.last_user_id
                if isinstance(last_id, str) and last_id.startswith('community_'):
                    # Формат: community_ID_INDEX
                    parts = last_id.split('_')
                    if len(parts) >= 2:
                        last_community_id = parts[1]
                        logger.info(f"Найдено прерванное состояние для сообщества {last_community_id}")
            
            # Собираем данные из друзей, если указан start_user_id
            if self.config.start_user_id:
                has_data_sources = True
                logger.info(f"Сбор данных по графу друзей начиная с пользователя {self.config.start_user_id}")
                
                # Если есть незавершенные пользователи, обрабатываем их первыми
                start_users = self.in_progress_users.copy() if self.in_progress_users else [self.config.start_user_id]
                
                tasks = []
                for user_id in start_users:
                    task = self.collect_friends(user_id)
                    tasks.append(task)
                
                await asyncio.gather(*tasks)
            
            # Собираем данные из сообществ, если они указаны
            if self.config.communities_ids:
                has_data_sources = True
                logger.info(f"Начинаем сбор данных из {len(self.config.communities_ids)} сообществ")
                
                # Сначала обрабатываем сообщество, на котором остановились (если такое есть)
                if last_community_id and last_community_id in self.config.communities_ids:
                    logger.info(f"Возобновление сбора с сообщества {last_community_id}")
                    await self.collect_community_members(last_community_id)
                    
                    # Создаем список оставшихся сообществ
                    remaining_communities = [
                        comm_id for comm_id in self.config.communities_ids 
                        if comm_id != last_community_id
                    ]
                else:
                    remaining_communities = self.config.communities_ids
                
                # Запускаем обработку оставшихся сообществ
                community_tasks = []
                for community_id in remaining_communities:
                    task = self.collect_community_members(community_id)
                    community_tasks.append(task)
                
                if community_tasks:
                    await asyncio.gather(*community_tasks)
            
            # Проверяем, был ли хотя бы один источник данных
            if not has_data_sources:
                logger.warning("Не указаны источники данных! Необходимо задать start_user_id или communities_ids в конфигурации.")
                return
            
            # Сохраняем оставшиеся данные
            if self.batch_data:
                self.storage.save_batch(self.batch_data, self.batch_index)
            
            logger.info(f"Сбор данных завершен. Всего собрано пользователей: {self.users_counter}")
            
            # Очищаем состояние после успешного завершения
            self.state_manager.clear_state()
            
        except KeyboardInterrupt:
            logger.warning("Сбор данных прерван пользователем")
            self._save_current_state()
        except Exception as e:
            logger.error(f"Ошибка во время сбора данных: {e}")
            self._save_current_state()
            raise
        finally:
            self.storage.cleanup_temp()
            
            if self.need_save_state:
                self._save_current_state() 