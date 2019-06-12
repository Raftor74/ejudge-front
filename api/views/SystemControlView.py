from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test
from tools import Response, EjudgeSystemControl


@user_passes_test(lambda u: u.is_superuser)
def system_start(request):
    EjudgeSystemControl().start_system()
    response = Response(Response.STATUS_OK, "", {}).get()
    return JsonResponse(response)


@user_passes_test(lambda u: u.is_superuser)
def system_stop(request):
    EjudgeSystemControl().stop_system()
    response = Response(Response.STATUS_OK, "", {}).get()
    return JsonResponse(response)


@user_passes_test(lambda u: u.is_superuser)
def system_reload(request):
    EjudgeSystemControl().reload_system()
    response = Response(Response.STATUS_OK, "", {}).get()
    return JsonResponse(response)


@user_passes_test(lambda u: u.is_superuser)
def system_status(request):
    processes_status = EjudgeSystemControl().get_system_processes_status()
    response = Response(Response.STATUS_OK, "", processes_status).get()
    return JsonResponse(response)