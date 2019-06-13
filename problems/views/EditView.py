from django.conf import settings
from django.shortcuts import render, get_object_or_404, reverse
from django.views import View
from django.http import JsonResponse
from tools import staff_required, Response, ProblemSerializer
from problems.models import Problems


@staff_required()
class EditView(View):

    def get(self, request, task_id):
        problem = get_object_or_404(Problems, pk=task_id)
        context = {
            'problem': problem,
            'checkers': settings.EJUDGE_CHECKERS_CHOICES,
        }
        return render(request, template_name='problems/edit.html', context=context)

    def post(self, request, task_id):

        if 'get_problem' in request.POST:
            problem = Problems.objects.get(pk=task_id)
            problem_dict = ProblemSerializer(problem).get_dict()
            response = Response(Response.STATUS_OK, "", problem_dict).get()
            return JsonResponse(response)

        data = {'redirect': reverse('problems_index')}
        response = Response(Response.STATUS_OK, "", data).get()
        return JsonResponse(response)