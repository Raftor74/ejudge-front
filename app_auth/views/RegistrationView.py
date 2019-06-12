from django.shortcuts import render, redirect, reverse
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login
from tools import Response, UserRegistration


# Регистрация пользователя
class RegistrationView(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('profile'))

        context = {}
        return render(request, template_name='app_auth/registration.html', context=context)

    def post(self, request):
        response_status = Response.STATUS_OK
        response_error = ''
        response_data = {}

        provider = UserRegistration(request.POST)
        created_user = provider.register()

        if not isinstance(created_user, User):
            response_status = Response.STATUS_FAIL
            response_error = provider.last_error
            response = Response(response_status, response_error, {}).get()
            return JsonResponse(response)

        login(request, user=created_user)

        response = Response(response_status, response_error, response_data).get()
        return JsonResponse(response)