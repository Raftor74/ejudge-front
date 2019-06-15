from ejudge_models.models import Users

class ContestRegisterManager(object):

    def __init__(self, user, contest, post_data):
        self.contest = contest
        self.user = user
        self.secret_word = post_data.get('secret_word', '')
        self.username_on_contest = post_data.get('username', '')
        self.last_error = ''
        self.ejudge_profile = None
        self.ejudge_user = None

    def check_secret_word(self):
        if not self.contest.is_closed:
            return True
        if self.secret_word == self.contest.secret_word:
            return True
        raise Exception("Неверное кодовое слово для соревнования")

    def check_user(self):
        if not hasattr(self.user, 'ejudgeprofile'):
            raise Exception("Не существует профиля Ejudge. Обратитесь к администратору")

        ejudge_profile = self.user.ejudgeprofile

        if not hasattr(ejudge_profile, 'ejudge_user'):
            raise Exception("Не существует логина для профиля Ejudge. Обратитесь к администратору")

        self.ejudge_user = ejudge_profile.ejudge_user
        self.ejudge_profile = ejudge_profile

        return True

    def register_user(self):
        self.contest.users.add(self.user)
        return True

    def save_username_on_contest(self):
        if not len(self.contest.ejudge_id):
            return False

        if not self.ejudge_user:
            return False

        if not self.ejudge_profile:
            return False

        contest_ejudge_id = int(self.contest.ejudge_id)
        ejudge_user = self.ejudge_user
        ejudge_profile = self.ejudge_profile
        username = self.username_on_contest

        try:
            user_instance = Users.objects.get(user=ejudge_user, contest_id=contest_ejudge_id)
            user_instance.username = username
            user_instance.save()
        except Users.DoesNotExist:
            user_instance = Users.objects.create(
                user=ejudge_user,
                contest_id=contest_ejudge_id,
                instnum=-1,
                username=username,
                cnts_read_only=0,
                pwdmethod=ejudge_profile.ejudge_pwdmethod
            )

        return True

    def register_user_on_contest(self):
        try:
            self.check_secret_word()
            self.check_user()
            self.save_username_on_contest()
            self.register_user()
        except Exception as e:
            self.last_error = str(e)
            return False

        return True
