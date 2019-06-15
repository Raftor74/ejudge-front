from django.urls import path
from .views import *

urlpatterns = [
    path('deploy/<contest_id>/', DeployView.as_view(), name='contests_deploy'),
    path('detail/<contest_id>/', DetailView.as_view(), name='contests_detail'),
    path('edit/<contest_id>/', EditView.as_view(), name='contests_edit'),
    path('create/', CreateView.as_view(), name='contests_create'),
    path('', IndexView.as_view(), name='contests_index'),
]