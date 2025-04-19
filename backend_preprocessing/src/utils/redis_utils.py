import time
import redis
from utils.config import Config

def wait_for_redis():
    """Wait for Redis to become available."""
    print("🌟 Waiting for Redis to be ready...")
    r = redis.Redis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)
    start = time.time()
    timeout = 30
    while True:
        try:
            if r.ping():
                print("Redis is up!")
                return
        except Exception as e:
            if time.time() - start > timeout:
                raise RuntimeError("Timeout waiting for Redis") from e
            print(f"Waiting for Redis. Host: {Config.REDIS_HOST}, Port: {Config.REDIS_PORT}")
            time.sleep(2)