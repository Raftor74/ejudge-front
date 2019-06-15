from django.shortcuts import render
from django.views import View
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from contests.models import Contests


class IndexView(LoginRequiredMixin, View):

    def get(self, request):
        user = request.user
        user_is_staff = request.user.is_staff
        page_size = 10
        current_page = request.GET.get('page', 1)

        if user_is_staff:
            contests = Contests.objects.order_by('-created_at').all()
        else:
            contests = Contests.objects\
                .order_by('-created_at')\
                .filter(is_visible=True)\
                .exclude(users__contests__users__exact=user)\
                .all()

        contests = Paginator(contests, page_size)
        contests = contests.get_page(current_page)

        context = {
            'contests': contests
        }

        return render(request, template_name='contests/index.html', context=context)