from sandbox.enums import DBAliasesEnum
from sandbox.utils import get_env_variable

DATABASES = {
    DBAliasesEnum.DEFAULT: {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_env_variable('DATABASE_NAME'),
        'USER': get_env_variable('DATABASE_USER'),
        'PASSWORD': get_env_variable('DATABASE_PASSWORD'),
        'HOST': get_env_variable('DATABASE_CONTAINER_HOST'),
        'PORT': get_env_variable('DATABASE_CONTAINER_PORT'),
    },
}
