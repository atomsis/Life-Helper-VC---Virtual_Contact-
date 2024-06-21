import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chat.routing import websocket_urlpatterns


# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VC.settings')
#
# django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
     # 'http': django_asgi_app,
     'websocket': AuthMiddlewareStack(
          URLRouter(
               websocket_urlpatterns
          )
     )
})