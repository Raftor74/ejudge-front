from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from contests.models import Contests
from django.core.paginator import Paginator


# Профиль
class IndexView(LoginRequiredMixin, View):

    def get(self, request):
        page_size = 10
        current_page = request.GET.get('page', 1)

        user = User.objects.get(pk=request.user.pk)
        count_contests = Contests.objects.filter(is_visible=True).count()
        user_contests = Contests.objects.order_by('-pk').filter(is_visible=True, users__contests__users__exact=user)
        user_contests = Paginator(user_contests, page_size)
        user_contests = user_contests.get_page(current_page)

        context = {
            'user': user,
            'count_contests': count_contests,
            'user_contests': user_contests,
        }

        return render(request, template_name='app_profile/index.html', context=context)