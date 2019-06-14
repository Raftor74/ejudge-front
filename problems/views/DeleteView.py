from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import View
from problems.models import Problems
from tools import staff_required


@staff_required()
class DeleteView(View):

    def get(self, request, task_id):
        problem = get_object_or_404(Problems, pk=task_id)
        context = {'problem': problem}
        return render(request, template_name='problems/delete.html', context=context)

    def post(self, request, task_id):
        problem = get_object_or_404(Problems, pk=task_id)
        problem.delete()
        return redirect(reverse('problems_index'))
