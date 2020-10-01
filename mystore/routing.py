from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import OriginValidator
from django.conf import settings

import notifications.routing

application = ProtocolTypeRouter({
    'websocket': OriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                notifications.routing.websocket_urlpatterns
            )
        ),
        ['*']
    ),
})
