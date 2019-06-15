from django.shortcuts import render, get_object_or_404
from django.views import View
from contests.models import Contests
from tools import admin_required
from contests.classes import ContestDeploy

@admin_required()
class DeployView(View):

    def get(self, request, contest_id):
        contest = get_object_or_404(Contests, pk=contest_id)
        ContestDeploy(contest).deploy()
        context = {'contest': contest}
        return render(request, template_name='contests/deploy.html', context=context)
