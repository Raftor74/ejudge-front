from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


class CreateView(LoginRequiredMixin, View):

    def get(self, request):
        context = {}
        return render(request, template_name='problems/create.html', context=context)
