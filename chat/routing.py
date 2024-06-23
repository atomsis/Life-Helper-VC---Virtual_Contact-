# from django.urls import path
# from . import consumers
#
# websocket_urlpatterns = [
#     path('ws/chat/<str:username>/', consumers.ChatConsumer.as_asgi()),
# ]

from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<user_id>\d+)/$', consumers.ChatConsumer.as_asgi()),
]
