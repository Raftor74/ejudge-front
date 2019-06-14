from django.shortcuts import render, get_object_or_404
from django.views import View
from contests.models import Contests
from tools import admin_required


@admin_required()
class DetailView(View):

    def get(self, request, contest_id):

        if request.user.is_staff:
            contest = get_object_or_404(Contests, pk=contest_id)
        else:
            contest = get_object_or_404(Contests, pk=contest_id, is_visible=True)

        context = {'contest': contest}
        return render(request, template_name='contests/detail.html', context=context)
