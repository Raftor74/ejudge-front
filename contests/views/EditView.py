from django.conf import settings
from django.shortcuts import render, get_object_or_404, reverse
from django.views import View
from django.http import JsonResponse
from tools import admin_required, Response, ContestSerializer, ContestUpdate
from contests.models import Contests


@admin_required()
class EditView(View):

    def get(self, request, contest_id):
        contest = get_object_or_404(Contests, pk=contest_id)
        context = {
            'contest': contest,
            'contests_types': settings.EJUDGE_CONTESTS_TYPES
        }
        return render(request, template_name='contests/edit.html', context=context)

    def post(self, request, contest_id):

        if 'get_contest' in request.POST:
            contest = Contests.objects.get(pk=contest_id)
            contest_dict = ContestSerializer(contest).get_dict()
            response = Response(Response.STATUS_OK, "", contest_dict).get()
            return JsonResponse(response)

        provider = ContestUpdate(contest_id, request.POST)
        updated_contest = provider.update_contest()

        if not isinstance(updated_contest, Contests):
            response_status = Response.STATUS_FAIL
            response_error = provider.last_error
            response = Response(response_status, response_error, {}).get()
            return JsonResponse(response)

        data = {'redirect': reverse('contest_detail', kwargs={'contest_id': contest_id})}
        response = Response(Response.STATUS_OK, "", data).get()
        return JsonResponse(response)