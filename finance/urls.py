from django.urls import path
from .views import send_money, deposit

app_name = 'finance'

urlpatterns = [
    path('send_money/<int:friend_id>/', send_money, name='send_money'),
    path('deposit/', deposit, name='deposit'),
]
