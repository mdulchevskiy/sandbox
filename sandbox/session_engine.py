from django.contrib.auth import SESSION_KEY
from django.contrib.sessions.backends.cached_db import SessionStore as BaseSessionStore
from django.contrib.sessions.models import AbstractBaseSession
from django.db import models


KEY_PREFIX = 'sandbox.session_engine'


class UserSession(AbstractBaseSession):
    user = models.ForeignKey('sandbox.User', null=True, related_name='sessions_rel', on_delete=models.CASCADE)

    class Meta(AbstractBaseSession.Meta):
        app_label = 'sandbox'
        verbose_name = 'User session'
        verbose_name_plural = 'User sessions'

    @classmethod
    def get_session_store_class(cls):
        return BaseSessionStore


class SessionStore(BaseSessionStore):
    cache_key_prefix = KEY_PREFIX

    @classmethod
    def get_model_class(cls):
        return UserSession

    def create_model_instance(self, data):
        obj = super().create_model_instance(data)

        try:
            user_id = int(data.get(SESSION_KEY))
        except (ValueError, TypeError):
            user_id = None

        obj.user_id = user_id

        return obj
