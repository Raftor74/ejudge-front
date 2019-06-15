from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import JsonResponse
from contests.models import Contests
from tools import admin_required, Response
from contests.classes import ContestDeploy

@admin_required()
class DeployView(View):

    def get(self, request, contest_id):
        contest = get_object_or_404(Contests, pk=contest_id)
        ContestDeploy(contest).deploy()
        context = {'contest': contest}
        return render(request, template_name='contests/deploy.html', context=context)


    def post(self, request, contest_id):
        contest = get_object_or_404(Contests, pk=contest_id)

        response_status = Response.STATUS_OK
        response_error = ''
        response_data = {}

        if 'deploy' in request.POST:
            success = ContestDeploy(contest).deploy()

        if 'remove' in request.POST:
            success = ContestDeploy(contest).remove()

        if 'reload' in request.POST:
            provider = ContestDeploy(contest)
            provider.remove()
            provider.deploy()

        if 'status' in request.POST:
            response_data = ContestDeploy(contest).get_contest_deploy_status()

        response = Response(response_status, response_error, response_data).get()
        return JsonResponse(response)
