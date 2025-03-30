import redis

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=False)

def get_redis_client():
    return redis_client
