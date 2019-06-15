from django.shortcuts import render
from django.views import View
from tools import staff_required


@staff_required()
class IndexView(View):

    def get(self, request):
        context = {}
        return render(request, template_name='system_control/index.html', context=context)