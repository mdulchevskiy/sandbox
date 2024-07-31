from sandbox.utils import get_env_variable

CACHE_URL = (f'redis://{get_env_variable("CACHE_CONTAINER_HOST")}:'
             f'{get_env_variable("CACHE_CONTAINER_PORT")}/'
             f'{get_env_variable("CACHE_DB")}')

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': CACHE_URL,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
