def media_url(request):
    from django.conf import settings
    return {'media_url': settings.MEDIA_URL,
            'root_url': settings.URL_ROOT,
            'current_path': request.path}
