# Generated by Django 5.0.7 on 2024-07-30 15:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sandbox', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSession',
            fields=[
                ('session_key', models.CharField(max_length=40, primary_key=True, serialize=False, verbose_name='session key')),
                ('session_data', models.TextField(verbose_name='session data')),
                ('expire_date', models.DateTimeField(db_index=True, verbose_name='expire date')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sessions_rel', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User session',
                'verbose_name_plural': 'User sessions',
                'abstract': False,
            },
        ),
    ]