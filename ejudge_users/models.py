from django.db import models
from django.contrib.auth.models import User
from ejudge_models.models import Logins, Cntsregs, Users
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver


# Спец. класс для Ejudge поля
class EjudgeForeginKey(models.ForeignKey):

    def db_type(self, connection):
        return 'INT UNSIGNED'


# Профиль пользователя в системе Ejudge
class EjudgeProfile(models.Model):

    # Типы методов шифрования в Ejudge
    PLAIN = '0'
    BASE64 = '1'
    SHA1 = '2'

    DEFAULT_PWD_METHOD = PLAIN

    EJUDGE_PWD_METHODS = (
        (PLAIN, 'Plain'),
        (BASE64, 'Base 64'),
        (SHA1, 'SHA-1'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Связанный пользователь')
    ejudge_user = EjudgeForeginKey(Logins, null=True, on_delete=models.SET_NULL, verbose_name='Пользователь в системе Ejudge')
    ejudge_password = models.CharField(max_length=255, blank=True, verbose_name='Пароль в системе Ejudge')
    ejudge_pwdmethod = models.CharField(max_length=2, choices=EJUDGE_PWD_METHODS, verbose_name='Тип шифрования')

    def __str__(self):
        if hasattr(self, 'user'):
            return self.user.username
        else:
            return self.pk

    @staticmethod
    def parse_pwd_method(pwd_method, default=DEFAULT_PWD_METHOD):
        try:
            return int(pwd_method)
        except ValueError:
            return default

    @property
    def ejudge_id(self):
        if hasattr(self, 'ejudge_user'):
            return self.ejudge_user.pk
        else:
            return None

    def save(self, *args, **kwargs):
        if hasattr(self, 'ejudge_user'):
            ejudge_user_model = self.ejudge_user
            ejudge_user_model.pwdmethod = 0
            ejudge_user_model.password = self.ejudge_password
            ejudge_user_model.pwdmethod = self.parse_pwd_method(self.ejudge_pwdmethod)
            ejudge_user_model.save()
        super(EjudgeProfile, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Профиль Ejudge'
        verbose_name_plural = 'Профили Ejudge'

    @staticmethod
    def save_profile(user_instance):
        if not user_instance:
            return False

        ejudge_user_model = Logins.objects.create(
            login=user_instance.username,
            email=user_instance.email,
        )

        return EjudgeProfile.objects.create(user=user_instance, ejudge_user=ejudge_user_model)

    @staticmethod
    def update_profile(user_instance):

        if not user_instance:
            return False

        if not hasattr(user_instance, 'ejudgeprofile'):
            return False

        # Модель EjudgeProfile
        ejudge_profile = user_instance.ejudgeprofile
        ejudge_profile.save()

        if not hasattr(ejudge_profile, 'ejudge_user'):
            return False

        # Модель Logins
        ejudge_user_model = ejudge_profile.ejudge_user

        # Заполнение полей в модели Logins
        ejudge_user_model.login = user_instance.username
        ejudge_user_model.email = user_instance.email
        ejudge_user_model.pwdmethod = EjudgeProfile.parse_pwd_method(ejudge_profile.ejudge_pwdmethod)
        ejudge_user_model.password = ejudge_profile.ejudge_password

        return ejudge_user_model.save()

    @receiver(post_save, sender=User)
    def create_ejudge_profile(sender, instance, created, **kwargs):
        if created:
            EjudgeProfile.save_profile(user_instance=instance)

    @receiver(post_save, sender=User)
    def save_ejudge_profile(sender, instance, **kwargs):
        EjudgeProfile.update_profile(user_instance=instance)


# Удаление связанных сущностей после удаления профиля Ejudge
@receiver(pre_delete, sender=EjudgeProfile)
def delete_ejudge_profile_model(sender, instance, **kwargs):
    ejudge_user_model_pk = instance.ejudge_id
    if ejudge_user_model_pk:
        # Получение модели пользователя
        ejudge_user_model = Logins.objects.get(pk=ejudge_user_model_pk)
        # Удаление регистрации пользователя на контесты
        Cntsregs.objects.filter(user=ejudge_user_model).delete()
        # Удаление всех данных пользователя
        Users.objects.filter(user=ejudge_user_model).delete()
        # Удаление самого пользователя
        ejudge_user_model.delete()