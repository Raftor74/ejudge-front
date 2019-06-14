import os
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from problems.models import Problems


# Таблица для хранения контестов
class Contests(models.Model):
    name = models.CharField(null=False, max_length=40, verbose_name="Название")
    ejudge_id = models.CharField(null=False, unique=True, max_length=10, verbose_name="ID в системе Ejudge")
    scope_system = models.CharField(blank=True, choices=settings.EJUDGE_CONTESTS_TYPES, max_length=10, verbose_name="Тип контеста")
    start_time = models.DateTimeField(null=True, verbose_name="Дата начала")
    duration = models.IntegerField(null=True, blank=True, verbose_name="Длительность в минутах")
    is_closed = models.BooleanField(default=False, verbose_name="Закрытый контест")
    is_visible = models.BooleanField(default=True, verbose_name="Доступен в списке")
    secret_word = models.CharField(blank=True, max_length=40, verbose_name="Кодовое слово")
    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, verbose_name="Создатель")
    problems = models.ManyToManyField(Problems, verbose_name="Список задач")
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, blank=True, verbose_name="Дата обновления")

    @property
    def contest_dir(self):
        return os.path.join(settings.EJUDGE_CONTESTS_DIR, self.ejudge_id)

    @property
    def config_dir(self):
        return os.path.join(self.contest_dir, 'conf')

    @property
    def config_path(self):
        return os.path.join(self.config_dir, 'serve.cfg')

    @property
    def problems_dir(self):
        return os.path.join(self.contest_dir, 'problems')

    @property
    def xml_config(self):
        return os.path.join(settings.EJUDGE_CONTESTS_CONFIG_DIR, "{}.xml".format(self.ejudge_id))

    def __str__(self):
        return "%s" % self.name

    class Meta:
        db_table = 'contests'
        verbose_name = 'Контест'
        verbose_name_plural = 'Контесты'

