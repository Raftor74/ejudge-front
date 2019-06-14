from ejudge_models.models import Cntsregs, Logins
from django.conf import settings
from django.contrib.auth.models import User


class ContestUserRegister(object):

    def __init__(self, contest_instance, user_set_ids, action):
        self.instance = contest_instance
        self.user_set_ids = user_set_ids
        self.action = action

    def resolve_action(self):
        if self.action == 'post_add':
            self.register_users_to_contest()
        elif self.action == 'post_remove':
            self.remove_users_from_contest()
        elif self.action == 'post_clear':
            self.remove_all_users_from_contest()

    def get_user_instance(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

        return user

    def is_user_admin(self, ejudge_user_id):
        return settings.EJUDGE_ADMIN_ID == ejudge_user_id

    def is_register_exist(self, contest_id, ejudge_user):
        return Cntsregs.objects.filter(user=ejudge_user, contest_id=contest_id).count()

    def remove_all_users_from_contest(self):
        contest_ejudge_id = int(self.instance.ejudge_id)
        try:
            ejudge_admin = Logins.objects.get(pk=settings.EJUDGE_ADMIN_ID)
        except Logins.DoesNotExist:
            return False
        try:
            Cntsregs.objects.filter(contest_id=contest_ejudge_id).exclude(user=ejudge_admin).delete()
        except Exception:
            return False

        return True

    def register_user_to_contest(self, user, contest_id):
        Cntsregs.objects.create(user=user, contest_id=contest_id, status=0)

    def remove_user_from_contest(self, user, contest_id):
        Cntsregs.objects.filter(user=user, contest_id=contest_id).delete()

    def register_users_to_contest(self):
        contest_ejudge_id = int(self.instance.ejudge_id)
        for user_id in self.user_set_ids:
            user = self.get_user_instance(user_id)

            if not isinstance(user, User):
                continue

            ejudge_user = user.ejudgeprofile.ejudge_user

            if not isinstance(ejudge_user, Logins):
                continue

            if self.is_register_exist(contest_ejudge_id, ejudge_user):
                continue

            self.register_user_to_contest(ejudge_user, contest_ejudge_id)
            return True

    def remove_users_from_contest(self):
        contest_ejudge_id = int(self.instance.ejudge_id)

        for user_id in self.user_set_ids:
            user = self.get_user_instance(user_id)

            if not isinstance(user, User):
                continue

            ejudge_user = user.ejudgeprofile.ejudge_user

            if not isinstance(ejudge_user, Logins):
                continue

            if not self.is_register_exist(contest_ejudge_id, ejudge_user):
                continue

            if self.is_user_admin(ejudge_user.pk):
                continue

            self.remove_user_from_contest(ejudge_user, contest_ejudge_id)
            return True