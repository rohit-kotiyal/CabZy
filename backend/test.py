from app.core.redis import redis_client

redis_client.flushdb()
print("DB FLushed")