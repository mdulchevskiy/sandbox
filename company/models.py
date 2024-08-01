from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

from sandbox.utils.enums import TimezoneEnum


class Company(models.Model):
    location = models.OneToOneField('sandbox.Location', null=True, on_delete=models.SET_NULL)
    company_name = models.CharField(max_length=255, verbose_name='Company title', unique=True)
    timezone = models.CharField(max_length=255, choices=TimezoneEnum.for_choice(), default=TimezoneEnum.UTC)

    def delete(self, *args, **kwargs):
        if self.location:
            self.location.delete()

        return super(self.__class__, self).delete(*args, **kwargs)

    def __str__(self):
        return f'{self.id}. {self.company_name}'


@receiver(post_delete, sender=Company)
def post_delete_location(sender, instance, *args, **kwargs):
    if instance.location:
        instance.location.delete()


class Employee(models.Model):
    base_user = models.OneToOneField('sandbox.User', related_name='company_user', on_delete=models.CASCADE)
    company = models.ForeignKey('company.Company', null=True, related_name='employees_rel', on_delete=models.CASCADE)

    hire_date = models.DateField(null=True)

    def __str__(self):
        return f'{self.id}. {self.user.username}'
