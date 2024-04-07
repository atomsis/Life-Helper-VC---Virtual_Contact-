from django.shortcuts import render
import requests
from django.http import JsonResponse
from .models import City

def get_weather(city):
    api_key = '5e39e0ae994d1a41a433fccde5f07786'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    data = response.json()
    return data

def weather(request, city_name):
    city = City.objects.get(name=city_name)
    data = get_weather(city.name)
    return JsonResponse(data)