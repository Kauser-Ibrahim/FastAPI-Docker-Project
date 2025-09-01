import json
import redis
from dotenv import load_dotenv
from app.core.config import settings

load_dotenv()
REDIS_URL = os.getenv("REDIS_URL")
redis_client = redis.StrictRedis.from_url(REDIS_URL, decode_responses=True)


def get_cached_prediction(key: str):
    value = redis_client.get(key)
    if value:
        return json.loads(value)
    return None


def set_cached_prediction(key: str, value: dict, expire: int = 3600):
    redis_client.setex(key, expire, json.dumps(value))
