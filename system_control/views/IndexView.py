from django.shortcuts import render
from django.views import View
from tools import admin_required


@admin_required()
class IndexView(View):

    def get(self, request):
        context = {}
        return render(request, template_name='system_control/index.html', context=context)