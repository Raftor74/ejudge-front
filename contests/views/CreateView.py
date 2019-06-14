from django.conf import settings
from django.shortcuts import render, reverse
from django.views import View
from django.http import JsonResponse
from contests.models import Contests
from tools import admin_required, Response
from contests.classes import ContestCreate


@admin_required()
class CreateView(View):

    def get(self, request):
        context = {
            'contests_types': settings.EJUDGE_CONTESTS_TYPES
        }
        return render(request, template_name='contests/create.html', context=context)

    def post(self, request):

        user = request.user
        provider = ContestCreate(request.POST, user)
        created_problem = provider.create_contest()

        if not isinstance(created_problem, Contests):
            response_status = Response.STATUS_FAIL
            response_error = provider.last_error
            response = Response(response_status, response_error, {}).get()
            return JsonResponse(response)

        data = {'redirect': reverse('contests_index')}
        response = Response(Response.STATUS_OK, "", data).get()
        return JsonResponse(response)

