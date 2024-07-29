import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Represents end-user of the portal. Used for authorization.
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
