# Generated by Django 2.2.1 on 2019-06-14 09:56

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contests', '0002_contests_is_visible'),
    ]

    operations = [
        migrations.AddField(
            model_name='contests',
            name='users',
            field=models.ManyToManyField(null=True, related_name='contest_users', to=settings.AUTH_USER_MODEL, verbose_name='Участники'),
        ),
    ]
