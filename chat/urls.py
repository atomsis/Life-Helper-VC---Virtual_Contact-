from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('chat/<int:user_id>/', views.chat, name='chat'),
    # path("<str:room_name>/", views.room, name="room")
]
