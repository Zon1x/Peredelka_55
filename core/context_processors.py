from django.conf import settings as django_settings

from .models import SiteSettings


def site_settings(request):
    try:
        settings = SiteSettings.objects.get()
    except SiteSettings.DoesNotExist:
        settings = None
    return {'site_settings': settings}


def asset_version(request):
    return {'ASSET_VERSION': getattr(django_settings, 'ASSET_VERSION', '1')}
