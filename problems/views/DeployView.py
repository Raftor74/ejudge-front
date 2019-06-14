import json
from django.shortcuts import render, get_object_or_404
from django.views import View
from problems.models import Problems
from tools import staff_required


@staff_required()
class DeployView(View):

    def get(self, request, task_id):
        problem = get_object_or_404(Problems, pk=task_id)

        try:
            problem.tests_examples = json.loads(problem.tests_examples)
        except json.JSONDecodeError:
            problem.tests_examples = list()

        context = {'problem': problem}
        return render(request, template_name='problems/deploy.html', context=context)
