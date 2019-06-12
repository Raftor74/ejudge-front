from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin


def staff_required():
    def wrapper(wrapped):
        class WrappedClass(UserPassesTestMixin, wrapped):
            def test_func(self):
                return self.request.user.is_staff

        return WrappedClass
    return wrapper


@staff_required()
class IndexView(View):

    def get(self, request):
        context = {}
        return render(request, template_name='system_control/index.html', context=context)