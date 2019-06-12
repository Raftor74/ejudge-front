from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(LoginRequiredMixin, View):

    def get(self, request):
        context = {}
        return render(request, template_name='problems/index.html', context=context)