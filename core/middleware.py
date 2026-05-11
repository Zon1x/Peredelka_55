"""Помощники middleware."""

from django.conf import settings


class NoCacheHtmlInDebugMiddleware:
    """В DEBUG не кэшировать HTML — иначе браузер может показывать старые шаблоны."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if getattr(settings, 'DEBUG', False) and response.get('Content-Type', '').startswith('text/html'):
            response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            response.headers['Pragma'] = 'no-cache'
        return response
