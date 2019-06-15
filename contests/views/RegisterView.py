from django.shortcuts import render, reverse, redirect
from django.views import View
from django.http import JsonResponse
from tools import admin_denied, Response
from contests.models import Contests


@admin_denied()
class RegisterView(View):

    def get(self, request, contest_id):
        user = request.user

        try:
            contest = Contests.objects.exclude(users__contests__users__exact=user).get(pk=contest_id, is_visible=True)
        except Contests.DoesNotExist:
            return redirect(reverse('contests_index'))

        if not contest.is_deployed:
            return redirect(reverse('contests_index'))

        context = {
            'contest': contest,
        }
        return render(request, template_name='contests/register.html', context=context)

    def post(self, request, contest_id):
        data = {'redirect': reverse('profile')}
        response = Response(Response.STATUS_OK, "", data).get()
        return JsonResponse(response)