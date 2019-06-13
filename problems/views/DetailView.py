from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


class DetailView(LoginRequiredMixin, View):

    def get(self, request, task_id):
        context = {'task_id': task_id}
        return render(request, template_name='problems/detail.html', context=context)
