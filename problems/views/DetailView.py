import json
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from problems.models import Problems


class DetailView(LoginRequiredMixin, View):

    def get(self, request, task_id):

        if request.user.is_staff:
            problem = get_object_or_404(Problems, pk=task_id)
        else:
            problem = get_object_or_404(Problems, pk=task_id, is_visible=True)

        try:
            problem.tests_examples = json.loads(problem.tests_examples)
        except json.JSONDecodeError:
            problem.tests_examples = list()

        context = {'problem': problem}
        return render(request, template_name='problems/detail.html', context=context)
