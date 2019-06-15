from django.shortcuts import render
from django.views import View


# Главная страница
class IndexView(View):

    def get(self, request):
        context = {}
        return render(request, template_name='main/index.html', context=context)