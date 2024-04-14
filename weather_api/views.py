import json
# from googletrans import Translator
from django.shortcuts import render, get_object_or_404
import requests
from django.http import JsonResponse,HttpResponseServerError
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

# def translate_city_name(city_name):
#     translator = Translator()
#     translation = translator.translate(city_name, src='en', dest='ru')
#     return translation.text

def weather(request,city_name):
    profile = get_object_or_404(Profile, user=request.user)
    city_name = profile.city
    # translated_city = translate_city_name(city)
    try:
        data = get_weather(city_name)
        # weather_data_struct = json.dumps(get_weather(city), indent=2)
        temperature = data['main']['temp']

        responce_data = {
            'temperature': round(temperature),
            'city': city_name,
            'description': translate_weather_description(data['weather'][0]['description']),
            'section':'weather',
        }
    except KeyError as e:
        error_message = f'KeyError: {e}'
        return  HttpResponseServerError(error_message)
    return render(request, 'weather_api.html', responce_data)
    # return f'На данный момент температура в Москве составляет {str(temperature)} градусов Цельсия'
