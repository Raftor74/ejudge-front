import json
from datetime import datetime
from problems.models import Problems
from ejudge_models.models import Logins
from django.contrib.auth.models import User
from django.conf import settings
from contests.models import Contests


class ContestBase (object):

    def __init__(self):
        self.id = ''
        self.name = ''
        self.ejudge_id = ''
        self.scope_system = ''
        self.start_time = ''
        self.start_time_format = "%d.%m.%Y %H:%M"
        self.duration = ''
        self.is_closed = False
        self.is_visible = True
        self.secret_word = ''
        self.owner = None
        self.problems = []
        self.last_error = ''


class ContestValidator(ContestBase):

    def __init__(self):
        super().__init__()
        self.validation_error = ''

    def validate_on_create(self):
        try:
            self.validate_name()\
                .validate_scope_system()\
                .validate_start_time()\
                .validate_duration()\
                .validate_problems()
        except Exception as e:
            self.validation_error = str(e)
            return False

        return True

    def validate_on_update(self):
        try:
            self.validate_name()\
                .validate_scope_system()\
                .validate_start_time()\
                .validate_duration()\
                .validate_problems()\
                .validate_on_contest_exist()
        except Exception as e:
            self.validation_error = str(e)
            return False

        return True

    def validate_on_not_empty_string(self, string):
        return len(string) > 0

    def validate_on_datetime(self, value):
        try:
            _datetime = datetime.strptime(value, self.start_time_format)
        except Exception:
            return False

        return True

    def validate_on_int(self, value):
        try:
            parse_success = int(value)
        except ValueError:
            return False

        return True

    def validate_name(self):
        if not self.validate_on_not_empty_string(self.name):
            raise Exception("Не указано название турнира")
        return self

    def validate_scope_system(self):
        if not self.validate_on_not_empty_string(self.scope_system):
            raise Exception("Не указано название турнира")
        return self

    def validate_start_time(self):
        if not self.validate_on_datetime(self.start_time):
            raise Exception("Неверный формат даты и времени начала турнира {}".format(self.start_time))
        return self

    def validate_duration(self):
        if not self.validate_on_int(self.duration):
            raise Exception("Неверный формат для времени турнира")

        if not int(self.duration) > 0:
            raise Exception("Не указано ограничение по времени")

        return self

    def validate_problems(self):
        self.problems = json.loads(self.problems)
        for problem in self.problems:
            id = problem['id']
            try:
                object = Problems.objects.get(pk=id)
            except Problems.DoesNotExist:
                raise Exception("Задача с ID: {} несуществует".format(id))

        return self

    def validate_on_contest_exist(self):
        try:
            contest = Contests.objects.get(pk=self.id)
        except Contests.DoesNotExist:
            raise Exception("Контест не существует")

        return self


class ContestCreate(ContestValidator):

    def __init__(self, post_data, owner=None):
        super().__init__()
        self.name = post_data.get('name', '')
        self.scope_system = post_data.get('scope_system', '')
        self.start_time = post_data.get('start_time', '')
        self.duration = post_data.get('duration', '')
        self.is_closed = post_data.get('is_closed', False)
        self.is_visible = post_data.get('is_visible', True)
        self.secret_word = post_data.get('secret_word', '')
        self.owner = owner
        self.problems = post_data.get('problems', '')
        self.last_error = ''

    def get_contest_problems(self):
        problems = list()
        for problem in self.problems:
            id = problem['id']
            object = Problems.objects.get(pk=id)
            problems.append(object)

        return problems

    def get_formated_ejudge_id(self, id):
        ejudge_id = str(id)
        while(len(ejudge_id) != 6):
            ejudge_id = '0' + ejudge_id
        return ejudge_id

    def get_start_time(self):
        return datetime.strptime(self.start_time, self.start_time_format)

    def get_ejudge_admin(self):
        ejudge_user = Logins.objects.get(pk=settings.EJUDGE_ADMIN_ID)
        admin_user = User.objects.get(ejudgeprofile__ejudge_user=ejudge_user)
        return admin_user

    def create_contest(self):
        if not self.validate_on_create():
            self.last_error = self.validation_error
            return False

        problems = self.get_contest_problems()
        admin_user = self.get_ejudge_admin()
        start_time = self.get_start_time()
        duration = int(self.duration)

        try:
            contest = Contests.objects.create(
                name=self.name,
                scope_system=self.scope_system,
                start_time=start_time,
                duration=duration,
                is_closed=bool(self.is_closed),
                is_visible=bool(self.is_visible),
                secret_word=self.secret_word,
                owner=self.owner
            )

            contest.ejudge_id = self.get_formated_ejudge_id(contest.pk)
            contest.save()
            contest.problems.add(*problems)
            contest.users.add(admin_user)
        except Exception as e:
            self.last_error = str(e)
            return False

        return contest


class ContestUpdate(ContestCreate):

    def __init__(self, contest_id, post_data):
        super().__init__(post_data)
        pass

    def update_contest(self):
        pass

