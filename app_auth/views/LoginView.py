from django.shortcuts import render
from django.views import View


# Авторизация пользователя
class LoginView(View):

    def get(self, request):
        context = {}
        return render(request, template_name='app_auth/login.html', context=context)