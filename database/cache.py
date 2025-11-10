import json

import redis.asyncio as redis
from typing import Optional
from config import *


class RedisClient:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=CACHE_HOST,
            port=CACHE_PORT,
            db=CACHE_DB,
            password=CACHE_PASSWORD,
            decode_responses=True,
            encoding="utf-8"
        )

    async def set_token(self, token: str, user_data: dict, expire_seconds: int = 3600):
        """Сохранить токен в Redis с данными пользователя"""
        await self.redis_client.setex(
            f"token:{token}",
            expire_seconds,
            json.dumps(user_data)
        )

    async def get_user_by_token(self, token: str) -> Optional[dict]:
        """Получить данные пользователя по токену"""
        data = await self.redis_client.get(f"token:{token}")
        if data:
            return json.loads(data)
        return None

    async def delete_token(self, token: str):
        """Удалить токен"""
        await self.redis_client.delete(f"token:{token}")

    async def token_exists(self, token: str) -> bool:
        """Проверить существование токена"""
        return await self.redis_client.exists(f"token:{token}") == 1

    async def set_user_tokens(self, user_id: str, tokens: list, expire_seconds: int = 3600):
        """Сохранить список токенов пользователя"""
        await self.redis_client.setex(
            f"user_tokens:{user_id}",
            expire_seconds,
            json.dumps(tokens)
        )

    async def get_user_tokens(self, user_id: str) -> list:
        """Получить токены пользователя"""
        data = await self.redis_client.get(f"user_tokens:{user_id}")
        if data:
            return json.loads(data)
        return []

    async def close(self):
        """Закрыть соединение"""
        self.redis_client.close()


# Создаем глобальный экземпляр
cache = RedisClient()
