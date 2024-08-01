import importlib
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from sandbox.utils.enums import (CountryDivisionEnum,
                                 CountryEnum, )


UserSession = importlib.import_module('sandbox.session_engine').UserSession


class User(AbstractUser):
    """
    Represents end-user of the portal. Used for authorization.
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)


class Location(models.Model):
    country = models.IntegerField(choices=CountryEnum.for_choice())
    state = models.CharField(choices=CountryDivisionEnum.for_choice())
    city = models.CharField(max_length=255, null=True)
    zip = models.CharField(max_length=10, null=True)
    address = models.CharField(max_length=255, null=True)
    full_address = models.CharField(max_length=1024, null=True)

    def get_full_address(self):
        return ', '.join(filter(bool, [
            self.address, self.city,
            CountryDivisionEnum.get_full_name(self.state),
            self.zip,
            CountryEnum.get_full_name(self.country),
        ]))

    def save(self, **kwargs):
        self.full_address = self.get_full_address()

        super(Location, self).save(**kwargs)

    def __str__(self):
        return f'{self.id}. {self.full_address}'
