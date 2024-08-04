from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'finance'

urlpatterns = [
    path('send_money/<int:friend_id>/', views.send_money, name='send_money'),
    path('deposit/', views.deposit, name='deposit'),
    path('success/', views.success, name='success'),
    path('cancel/', TemplateView.as_view(template_name='finance/cancel.html'), name='cancel'),
]
