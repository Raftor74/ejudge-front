from django.shortcuts import render
from django.views import View
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from problems.models import Problems


class IndexView(LoginRequiredMixin, View):

    def get(self, request):
        user_is_staff = request.user.is_staff
        page_size = 10
        current_page = request.GET.get('page', 1)

        if user_is_staff:
            problems = Problems.objects.order_by('-created_at').all()
        else:
            problems = Problems.objects.order_by('-created_at').filter(is_visible=True).all()

        problems = Paginator(problems, page_size)
        problems = problems.get_page(current_page)

        context = {
            'problems': problems
        }

        return render(request, template_name='problems/index.html', context=context)