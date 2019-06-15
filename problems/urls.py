from django.urls import path
from .views import *

urlpatterns = [
    path('delete/<task_id>/', DeleteView.as_view(), name='problems_delete'),
    path('detail/<task_id>/', DetailView.as_view(), name='problems_detail'),
    path('edit/<task_id>/', EditView.as_view(), name='problems_edit'),
    path('create/', CreateView.as_view(), name='problems_create'),
    path('', IndexView.as_view(), name='problems_index'),
]