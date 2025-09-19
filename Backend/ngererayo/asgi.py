# ngererayo/asgi.py
"""
ASGI config for ngererayo project.
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ngererayo.settings")

# Load Django first
django_asgi_app = get_asgi_application()

# Import AFTER Django setup
from market.routing import websocket_urlpatterns
from market.middleware import JWTAuthMiddleware

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": JWTAuthMiddleware(
        URLRouter(websocket_urlpatterns)
    ),
})
