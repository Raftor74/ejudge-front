from django.conf import settings
from django.shortcuts import render, reverse
from django.views import View
from django.http import JsonResponse
from problems.models import Problems
from tools import staff_required, Response, ProblemCreate


@staff_required()
class CreateView(View):

    def get(self, request):
        context = {
            'checkers': settings.EJUDGE_CHECKERS_CHOICES
        }
        return render(request, template_name='problems/create.html', context=context)

    def post(self, request):

        user = request.user
        provider = ProblemCreate(request.POST, user)
        created_problem = provider.create_problem()

        if not isinstance(created_problem, Problems):
            response_status = Response.STATUS_FAIL
            response_error = provider.last_error
            response = Response(response_status, response_error, {}).get()
            return JsonResponse(response)

        data = {'redirect': reverse('problems_index')}
        response = Response(Response.STATUS_OK, "", data).get()
        return JsonResponse(response)

