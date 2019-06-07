from django.shortcuts import redirect
from django.contrib.auth import logout
from django.urls import reverse


# Редирект на страницу Login со страницы Auth
def auth_redirect(request):
    return redirect(reverse('login'))


def auth_logout(request):
    logout(request)
    return redirect('/')