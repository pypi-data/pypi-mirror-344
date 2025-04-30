"""
Модуль для работы с API ВКонтакте.

Предоставляет класс клиента для взаимодействия с API ВКонтакте,
который позволяет получать информацию о пользователях, их друзьях,
постах и сообществах.

Основные методы:
- get_friends_ids: получение списка ID друзей пользователя
- get_users_info: получение информации о пользователях
- get_posts_batch: получение последних постов пользователей
- get_user_communities: получение списка сообществ пользователя
- get_communities_batch: получение сообществ для нескольких пользователей
"""
import time
import asyncio
import logging
import vk_api
import random
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)


class VKClient:
    """Клиент для работы с API ВКонтакте."""
    
    def __init__(self, access_token: str, request_delay: float = 0.35):
        """
        Инициализирует клиент VK API.
        
        Args:
            access_token: Токен доступа к API ВКонтакте
            request_delay: Задержка между запросами в секундах
        """
        self.access_token = access_token
        self.request_delay = request_delay
        self.vk_session = vk_api.VkApi(token=access_token)
        self.vk = self.vk_session.get_api()
    
    async def get_friends_ids(self, user_id: str) -> List[str]:
        """
        Асинхронно получает список ID друзей пользователя.
        
        Args:
            user_id: ID пользователя ВКонтакте
            
        Returns:
            List[str]: Список ID друзей
        """
        try:
            result = self.vk.friends.get(user_id=user_id).get("items", [])
            await asyncio.sleep(self.request_delay)
            return result
        except vk_api.ApiError as e:
            logger.error(f"Error getting friends for user {user_id}: {e}")
            return []
    
    async def get_users_info(self, user_ids: List[str]) -> List[Dict[str, Any]]:
        """
        Асинхронно получает информацию о пользователях.
        
        Args:
            user_ids: Список ID пользователей
            
        Returns:
            List[Dict[str, Any]]: Список профилей пользователей
        """
        fields = (
            "bdate, city, country, photo_max, photo_id, followers_count, sex, "
            "occupation, interests, education, universities, schools, domain, "
            "status, last_seen, relation, personal, connections, activities"
        )
        try:
            result = self.vk.users.get(user_ids=user_ids, fields=fields)
            await asyncio.sleep(self.request_delay)
            return result
        except vk_api.ApiError as e:
            logger.error(f"Error getting user info: {e}")
            return []
    
    async def get_posts_batch(self, user_ids: List[str]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Асинхронно получает посты пользователей батчами.
        
        Args:
            user_ids: Список ID пользователей
            
        Returns:
            Dict[str, List[Dict[str, Any]]]: Словарь с постами пользователей
        """
        results = {}
        batch_size = 25  # API VK ограничение
        
        for i in range(0, len(user_ids), batch_size):
            batch = user_ids[i : i + batch_size]
            code = "return [" + ",".join(
                f'API.wall.get({{"owner_id": {uid}, "count": 5}})' for uid in batch
            ) + "];"
            
            try:
                response = self.vk.execute(code=code)
                success_count = 0
                fail_count = 0
                
                for idx, posts in enumerate(response):
                    uid = batch[idx]
                    if isinstance(posts, dict):
                        items = posts.get("items", [])
                        results[uid] = items
                        success_count += 1
                    else:
                        results[uid] = []
                        fail_count += 1
                
                logger.info(
                    f"Batch [{i + 1}-{i + len(batch)}]: "
                    f"Success: {success_count}, Failed: {fail_count}"
                )
            
            except vk_api.ApiError as e:
                logger.error(f"Error executing batch request: {e}")
            
            await asyncio.sleep(self.request_delay)
        
        return results
        
    async def get_user_communities(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Асинхронно получает список сообществ пользователя.
        
        Args:
            user_id: ID пользователя ВКонтакте
            
        Returns:
            List[Dict[str, Any]]: Список сообществ пользователя
        """
        method = "groups.get"
        params = {
            "user_id": user_id,
            "extended": 1,
            "fields": "name,description,members_count",
            "access_token": self.access_token,
            "v": "5.131"
        }
        
        max_retries = 3
        retry_delay = 1
        
        for attempt in range(max_retries):
            try:
                await asyncio.sleep(random.uniform(0.3, 0.5))
                
                response = self.vk.groups.get(
                    user_id=user_id,
                    extended=1,
                    fields="name,description,members_count"
                )
                
                return response.get("items", [])
                
            except vk_api.VkApiError as e:
                error_code = getattr(e, "code", 0)
                error_msg = str(e)
                
                if error_code == 6:  # Too many requests per second
                    wait_time = 2 * (attempt + 1)
                    logger.warning(f"Too many requests for user {user_id}. Waiting {wait_time} seconds...")
                    await asyncio.sleep(wait_time)
                    continue
                    
                elif error_code == 18:  # User deleted or banned
                    logger.warning(f"User {user_id} deleted or banned.")
                    return []
                    
                elif error_code == 5:  # Auth error
                    logger.error(f"Authentication error: {error_msg}. Check your API token.")
                    return []
                
                else:
                    logger.error(f"API error for user {user_id}: {error_code} - {error_msg}")
                    if attempt < max_retries - 1:
                        await asyncio.sleep(retry_delay)
                        retry_delay *= 2
                        continue
                    return []
        
        return []
    
    async def get_communities_batch(self, user_ids: List[str]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Асинхронно получает сообщества пользователей батчами.
        
        Args:
            user_ids: Список ID пользователей
            
        Returns:
            Dict[str, List[Dict[str, Any]]]: Словарь с сообществами пользователей
        """
        results = {}
        
        for user_id in user_ids:
            communities = await self.get_user_communities(user_id)
            results[user_id] = communities
            
            await asyncio.sleep(self.request_delay)
        
        return results
        
    async def get_community_members(self, community_id: str, max_members: int = 10000) -> List[str]:
        """
        Асинхронно получает список ID участников сообщества.
        
        Args:
            community_id: ID сообщества ВКонтакте (без знака минус)
            max_members: Максимальное количество участников для получения
            
        Returns:
            List[str]: Список ID участников сообщества
        """
        all_members = []
        count = 1000  # Максимальное количество участников за один запрос
        offset = 0
        
        try:
            community_info = self.vk.groups.getById(
                group_id=community_id,
                fields="members_count"
            )[0]
            total_members = min(community_info.get("members_count", 0), max_members)
            logger.info(f"Сообщество {community_id} имеет {community_info.get('members_count', 0)} участников. "
                        f"Будет получено до {total_members}")
        except vk_api.VkApiError as e:
            logger.error(f"Ошибка при получении информации о сообществе {community_id}: {e}")
            return []
        
        while offset < total_members:
            try:
                response = self.vk.groups.getMembers(
                    group_id=community_id,
                    offset=offset,
                    count=count
                )
                
                members = response.get("items", [])
                
                if not members:
                    break
                    
                all_members.extend(members)
                offset += len(members)
                
                logger.info(f"Получено {len(members)} участников из сообщества {community_id}. "
                            f"Всего: {len(all_members)}/{total_members}")
                
                if len(all_members) >= max_members:
                    logger.info(f"Достигнут максимальный лимит участников для сообщества {community_id}: {max_members}")
                    break
                
                await asyncio.sleep(self.request_delay)
                
            except vk_api.VkApiError as e:
                error_code = getattr(e, "code", 0)
                error_msg = str(e)
                
                if error_code == 6:  # Too many requests per second
                    logger.warning(f"Слишком много запросов для сообщества {community_id}. Ожидание 2 секунд...")
                    await asyncio.sleep(2)
                    continue
                    
                elif error_code == 15:  # Access denied
                    logger.warning(f"Доступ запрещен к сообществу {community_id}.")
                    break
                    
                elif error_code == 5:  # Auth error
                    logger.error(f"Ошибка аутентификации: {error_msg}. Проверьте токен доступа.")
                    break
                
                else:
                    logger.error(f"Ошибка API для сообщества {community_id}: {error_code} - {error_msg}")
                    break
        
        logger.info(f"Завершен сбор участников для сообщества {community_id}. "
                    f"Всего собрано: {len(all_members)}")
        
        return all_members

    async def get_communities_members_batch(self, community_ids: List[str], max_members: int = 10000) -> Dict[str, List[str]]:
        """
        Асинхронно получает участников для нескольких сообществ.
        
        Args:
            community_ids: Список ID сообществ
            max_members: Максимальное количество участников для получения из каждого сообщества
            
        Returns:
            Dict[str, List[str]]: Словарь с ID участников для каждого сообщества
        """
        results = {}
        
        for community_id in community_ids:
            members = await self.get_community_members(community_id, max_members)
            results[community_id] = members
        
        return results 