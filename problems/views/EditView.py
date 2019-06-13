from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


class EditView(LoginRequiredMixin, View):

    def get(self, request, task_id):
        context = {}
        return render(request, template_name='problems/edit.html', context=context)