import json
from django.shortcuts import render, get_object_or_404
import requests
from django.http import JsonResponse
from .models import City
from account.models import Profile


def get_weather(city):
    api_key = '5e39e0ae994d1a41a433fccde5f07786'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    data = response.json()
    return data


def translate_weather_description(description):
    translations = {
        'clear sky': 'ясное небо',
        'few clouds': 'небольшая облачность',
        'scattered clouds': 'рассеянные облака',
        'broken clouds': 'облачно с прояснениями',
        'overcast clouds': 'пасмурно',
        'shower rain': 'небольшой дождь',
        'rain': 'дождь',
        'light rain': 'легкий дождь',
        'moderate rain': 'умеренный дождь',
        'heavy intensity rain': 'сильный дождь',
        'thunderstorm': 'гроза',
        'snow': 'снег',
        'mist': 'туман',
    }
    return translations.get(description, description)


def weather(request, city_name):
    profile = get_object_or_404(Profile, user=request.user)
    city = profile.city
    # city = City.objects.get(name=city_name)
    data = get_weather(city)
    weather_data_struct = json.dumps(get_weather(city), indent=2)
    # temperature = {'temp':data['main']['temp']}
    temperature = data['main']['temp']

    responce_data = {
        'temperature': round(temperature),
        'city': city,
        'description': data['weather'][0]['description'],
        'section':'weather',
    }
    return render(request, 'weather_api.html', responce_data)
    # return f'На данный момент температура в Москве составляет {str(temperature)} градусов Цельсия'
