from  django.urls import path
from . import views

urlpatterns = [
    path('<str:city_name>/',views.weather,name='weather')
]