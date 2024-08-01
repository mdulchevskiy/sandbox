from django.db import models
from django.db.models import Q
from django.db.models.expressions import RawSQL

from .functions import Epoch


class TimezoneManager(models.Manager):
    def get_queryset(self):
        return super(TimezoneManager, self).get_queryset().exclude(
            Q(name__startswith='posix/') |
            Q(name__startswith='Etc/') |
            Q(name__startswith='GMT') |
            Q(name__startswith='SystemV') |
            Q(name__in=('localtime', 'posixrules', 'Universal', 'US/Pacific-New')),
        ).order_by('name')


class TimezoneHumanizeManager(TimezoneManager):
    def get_queryset(self):
        return super(TimezoneHumanizeManager, self).get_queryset().annotate(
            utc_offset_seconds=Epoch('utc_offset'),
            utc_offset_human=RawSQL(
                "replace(replace('UTC+' || to_char(EXTRACT(HOURS FROM utc_offset), 'fm00') || ':'  || "
                "to_char(EXTRACT(MINUTES FROM utc_offset), 'fm00'), '+-', '-'), ':-', ':')",
                [],
                output_field=models.CharField(),
            ),
        )


class Timezone(models.Model):
    name = models.TextField(primary_key=True)
    abbrev = models.TextField()
    utc_offset = models.DateTimeField(verbose_name='UTC offset')
    is_dst = models.BooleanField(verbose_name='Is DST')

    objects = TimezoneManager()
    humanized = TimezoneHumanizeManager()

    class Meta:
        managed = False
        db_table = 'pg_timezone_names'
