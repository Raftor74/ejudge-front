import os
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.views import View
from problems.models import Problems
from tools import staff_required, ProblemDeploy


@staff_required()
class DeployView(View):

    def get(self, request, task_id):
        problem = get_object_or_404(Problems, pk=task_id)
        deploy_path = os.path.join(settings.BASE_DIR, 'test')
        short_id = 'A'
        provider = ProblemDeploy(deploy_path=deploy_path, short_id=short_id, problem=problem)
        provider.remove()
        provider.deploy()
        context = {'problem': problem}
        return render(request, template_name='problems/deploy.html', context=context)
