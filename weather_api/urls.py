from  django.urls import path
from . import views

app_name = 'weather_api'

urlpatterns = [
    path('<str:city_name>/',views.weather,name='weather')
    # path('', views.weather, name='weather')

]