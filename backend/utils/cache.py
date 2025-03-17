import json
import aioredis
from typing import Any, Optional

class RedisCache:
    def __init__(self, redis_url: str = "redis://localhost"):
        self.redis = aioredis.from_url(redis_url)

    async def get(self, key: str) -> Optional[Any]:
        value = await self.redis.get(key)
        if value:
            return json.loads(value)
        return None

    async def set(self, key: str, value: Any, expire: int = 3600) -> bool:
        try:
            await self.redis.set(key, json.dumps(value), ex=expire)
            return True
        except Exception as e:
            print(f"缓存设置失败: {str(e)}")
            return False

    async def delete(self, key: str) -> bool:
        return await self.redis.delete(key) > 0