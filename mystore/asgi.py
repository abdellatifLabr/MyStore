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

application = asgi_cors(get_asgi_application(), hosts=settings.CORS_ALLOWED_ORIGINS, allow_all=settings.CORS_ORIGIN_ALLOW_ALL)
