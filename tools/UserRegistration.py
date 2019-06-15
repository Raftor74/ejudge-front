from django.core.validators import validate_email
from django.contrib.auth.models import User
from ejudge_users.models import EjudgeProfile
import hashlib


class UserBase(object):

    def __init__(self):
        self.username = ''
        self.first_name = ''
        self.last_name = ''
        self.email = ''
        self.password = ''
        self.confirm_password = ''
        self.last_error = ''


class UserValidator(UserBase):

    def __init__(self):
        super().__init__()
        self.validation_error = ''

    def validate(self):
        try:
            self.validate_username()\
                .validate_first_name()\
                .validate_last_name()\
                .validate_email()\
                .validate_password()
        except Exception as e:
            self.validation_error = str(e)
            return False

        return True

    def validate_username(self):
        return self.validate_username_on_correct().validate_username_on_exist()

    def validate_username_on_correct(self):
        username_length = len(self.username)
        if username_length < 5 or username_length > 30:
            raise Exception("Длина логина должна быть от 5 до 30 символов")
        return self

    def validate_username_on_exist(self):
        try:
            user = User.objects.get(username=self.username)
        except User.DoesNotExist:
            return self

        raise Exception("Пользователь с таким Логином уже существует")

    def validate_first_name(self):
        first_name_length = len(self.first_name)
        if not first_name_length:
            raise Exception("Не указано Имя пользователя")
        return self

    def validate_last_name(self):
        last_name_length = len(self.last_name)
        if not last_name_length:
            raise Exception("Не указана Фамилия пользователя")
        return self

    def validate_email(self):
        return self.validate_email_on_correct().validate_email_on_exist()

    def validate_email_on_correct(self):
        try:
            validate_email(self.email)
        except validate_email.ValidationError:
            raise Exception('Указан некорректный Email')
        return self

    def validate_email_on_exist(self):
        try:
            user = User.objects.get(email=self.email)
        except User.DoesNotExist:
            return self

        raise Exception("Пользователь с таким Email уже существует")

    def validate_password(self):
        return self.validate_password_on_correct().compare_password_with_confirm()

    def validate_password_on_correct(self):
        password_length = len(self.password)
        if password_length < 8:
            raise Exception("Длина пароля менее 8 символов")
        return self

    def compare_password_with_confirm(self):
        if self.password != self.confirm_password:
            raise Exception("Пароли не совпадают")
        return self


class UserRegistration(UserValidator):

    """ Класс для регистрации пользователей в системе """

    def __init__(self, post_request):
        super().__init__()
        self.username = post_request.get('login', '')
        self.first_name = post_request.get('firstName', '')
        self.last_name = post_request.get('lastName', '')
        self.email = post_request.get('email', '')
        self.password = post_request.get('password', '')
        self.confirm_password = post_request.get('confirmPassword', '')

    def register(self):
        if not self.validate():
            self.last_error = self.validation_error
            return False

        user = self.create_user()

        if not isinstance(user, User):
            self.last_error = "Ошибка регистрации пользователя"
            return False

        return user

    def get_sha1_password(self):
        password = str(self.password).encode('utf-8')
        return hashlib.sha1(password).hexdigest()

    def create_user(self):
        django_user = self.create_user_in_django_app()
        ejudge_user = self.create_user_in_ejudge_app(django_user)
        return ejudge_user

    def create_user_in_django_app(self):
        user = User.objects.create_user(
            username=self.username,
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            password=self.password
        )

        return user

    def create_user_in_ejudge_app(self, django_user):
        django_user.ejudgeprofile.ejudge_password = self.get_sha1_password()
        django_user.ejudgeprofile.ejudge_pwdmethod = EjudgeProfile.SHA1
        django_user.save()
        return django_user
