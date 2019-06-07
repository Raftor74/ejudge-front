from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from django.contrib.auth import authenticate, login
from tools import Response


class LoginView(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/')

        context = {}
        return render(request, template_name='app_auth/login.html', context=context)

    def post(self, request):
        response_status = Response.STATUS_OK
        response_error = ''
        response_data = ''

        username = request.POST.get('login', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)

        if user is not None:
            if not user.is_active:
                response_status = Response.STATUS_FAIL
                response_error = "Аккаунт '{}' отключен. Обратитесь к администратору".format(username)
            else:
                login(request, user)
        else:
            response_status = Response.STATUS_FAIL
            response_error = "Неверные логин или пароль"

        response = Response(response_status, response_error, response_data).get()
        return JsonResponse(response)