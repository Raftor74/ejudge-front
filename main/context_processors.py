from django.conf import settings


# Передача настроек сайта в шаблоны
def site_settings(request):
    return {
        'SITE_NAME': settings.SITE_NAME,
        'SITE_URL': settings.SITE_URL,
        'FOOTER_COPYRIGHT': settings.FOOTER_COPYRIGHT,
    }