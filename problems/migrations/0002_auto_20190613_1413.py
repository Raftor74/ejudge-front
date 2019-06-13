# Generated by Django 2.2.1 on 2019-06-13 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='problems',
            name='is_visible',
            field=models.BooleanField(default=True, verbose_name='Доступна для просмотра пользователям'),
        ),
        migrations.AlterField(
            model_name='problems',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата обновления'),
        ),
    ]
