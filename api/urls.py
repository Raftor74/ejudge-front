from django.urls import path
from .views import *

urlpatterns = [
    path('system/control/start/', system_start, name='start_ejudge_system'),
    path('system/control/stop/', system_stop, name='stop_ejudge_system'),
    path('system/control/reload/', system_reload, name='reload_ejudge_system'),
    path('system/control/status/', system_status, name='ejudge_system_status'),
    path('problems/search/', TaskSearchView.as_view(), name='problems_search_api'),
]