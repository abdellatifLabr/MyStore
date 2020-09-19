"""
ASGI config for mystore project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os
from django.conf import settings
from asgi_cors import asgi_cors

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mystore.settings.dev')

def validate_origin(origin):
    if settings['CORS_ORIGIN_ALLOW_ALL']:
        return True

    return origin in settings['CORS_ALLOWED_ORIGINS']

application = asgi_cors(get_asgi_application(), callback=validate_origin)
