import os
import time
import redis


r = redis.from_url(os.getenv("REDIS_URL", "redis://redis:6379/0"))


if __name__ == "__main__":
    print("Worker started. (stub)")
    while True:
        # Placeholder: poll a queue or just heartbeat
        r.set("worker:heartbeat", int(time.time()))
        time.sleep(5)