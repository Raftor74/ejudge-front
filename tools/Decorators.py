from django.contrib.auth.mixins import UserPassesTestMixin


def staff_required():
    def wrapper(wrapped):
        class WrappedClass(UserPassesTestMixin, wrapped):
            def test_func(self):
                return self.request.user.is_staff

        return WrappedClass
    return wrapper