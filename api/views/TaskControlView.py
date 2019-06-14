from django.http import JsonResponse
from django.db.models import Q
from tools import Response
from django.views import View
from tools import admin_required
from problems.models import Problems


@admin_required()
class TaskSearchView(View):

    def post(self, request):
        query = request.POST.get('q', '')
        problems = Problems.objects.filter(Q(title__icontains=query) | Q(pk=query)).only("pk", "title").all()
        response_data = list()
        for problem in problems:
            response_data.append({
                'id': problem.pk,
                'title': problem.title,
                'text': "ID:{} {}".format(problem.pk, problem.title)
            })
        response = Response(Response.STATUS_OK, "", response_data).get()
        return JsonResponse(response)

