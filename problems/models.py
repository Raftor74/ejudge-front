from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField


# Задачи
class Problems(models.Model):
    title = models.CharField(max_length=40, blank=True, verbose_name="Название задачи")
    description = RichTextUploadingField(blank=True, default='', verbose_name="Описание задачи")
    epsilon = models.CharField(max_length=20, blank=True, default="0.01", verbose_name="Точность")
    max_vm_size = models.IntegerField(default=64, blank=True, verbose_name="Ограничение по памяти МБ")
    max_exec_time = models.IntegerField(default=5, blank=True, verbose_name="Ограничение времени исполнения (сек)")
    tests_examples = models.TextField(default='', blank=True, verbose_name="JSON с входными и выходными данными")
    tests = models.TextField(verbose_name="JSON с тестами")
    comparison = models.CharField(max_length=40, choices=settings.EJUDGE_CHECKERS_CHOICES, verbose_name="Тип сравнения")
    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, verbose_name="Создатель")
    is_visible = models.BooleanField(default=True, verbose_name="Доступна для просмотра пользователям")
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, blank=True, verbose_name="Дата обновления")

    def __str__(self):
        return "%s" % self.title

    class Meta:
        db_table = 'problems'
        verbose_name = 'Задачу'
        verbose_name_plural = 'Задачи'

