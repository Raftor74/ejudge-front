import os
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from ejudge_models.models import Cntsregs
from problems.models import Problems
from django.db.models.signals import m2m_changed
from django.db.models.signals import pre_delete
from tools import ContestUserRegister
from django.dispatch import receiver


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
    users = models.ManyToManyField(User, null=True, related_name='contest_users', verbose_name="Участники")
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

    @property
    def duration_formatted(self):
        hours = str(self.duration // 60)
        minutes = str(self.duration % 60)
        hours = '0' + hours if len(hours) == 1 else hours
        minutes = '0' + minutes if len(minutes) == 1 else minutes
        return "{}:{}:00".format(hours, minutes)

    def __str__(self):
        return "%s" % self.name

    class Meta:
        db_table = 'contests'
        verbose_name = 'Контест'
        verbose_name_plural = 'Контесты'


# Регистрируем пользователя на турнир в Ejudge, когда он регистрируется в Django
def contests_users_changed(sender, **kwargs):
    ContestUserRegister(
        contest_instance=kwargs['instance'],
        user_set_ids=kwargs['pk_set'],
        action=kwargs['action']
    ).resolve_action()


m2m_changed.connect(contests_users_changed, sender=Contests.users.through)


# Удаление связанных сущностей после удаления контеста Ejudge
@receiver(pre_delete, sender=Contests)
def delete_contest_records(sender, instance, **kwargs):
    ejudge_contest_id = int(instance.ejudge_id)
    Cntsregs.objects.filter(contest_id=ejudge_contest_id).delete()
