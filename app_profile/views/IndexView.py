from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin


# Профиль
class IndexView(LoginRequiredMixin, View):

    def get(self, request):
        user = User.objects.get(pk=request.user.pk)
        context = {'user':user}
        return render(request, template_name='app_profile/index.html', context=context)