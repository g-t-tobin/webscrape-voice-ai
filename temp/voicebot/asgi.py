import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from bot.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'voicebot.settings')
django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # ✅ Handle regular HTTP views
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})



