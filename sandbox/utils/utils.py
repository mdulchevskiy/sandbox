import os

from django.core.exceptions import ImproperlyConfigured


def get_env_variable(var_name, fallback=None):
    try:
        value = os.environ[var_name]
        if not value and fallback is not None:
            value = fallback
        return value

    except KeyError:
        if fallback is not None:
            return fallback

        error_msg = f'Set the {var_name} environment variable'
        raise ImproperlyConfigured(error_msg)


def str_to_bool(value):
    return value.lower() in ('yes', 'true', 't', '1')
