from django.conf import settings
from django.shortcuts import render, reverse
from django.views import View
from django.http import JsonResponse
from tools import staff_required, Response


@staff_required()
class CreateView(View):

    def get(self, request):
        context = {
            'checkers': settings.EJUDGE_CHECKERS_CHOICES
        }
        return render(request, template_name='problems/create.html', context=context)

    def post(self, request):
        data = {'redirect': reverse('problems_index')}
        response = Response(Response.STATUS_OK, "", data).get()
        return JsonResponse(response)

