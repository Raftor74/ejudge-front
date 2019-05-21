from django.shortcuts import render
from django.views import View


# Регистрация пользователя
class RegistrationView(View):

    def get(self, request):
        context = {}
        return render(request, template_name='app_auth/registration.html', context=context)