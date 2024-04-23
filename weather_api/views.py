import json
from django.shortcuts import render, get_object_or_404
import requests
from django.http import JsonResponse, HttpResponseServerError
from .models import City, Weather
from account.models import Profile
from datetime import datetime, timedelta


def kph_to_mps(kph):
    return kph * 1000 / 3600


def weather(request, city_name='Moscow'):
    profile = Profile.objects.get(user=request.user)
    if profile.city:
        city = profile.city
    else:
        city = 'Moscow'
    translated_city = translate_city_name(city)
    url = "https://weatherapi-com.p.rapidapi.com/forecast.json"
    querystring = {"q": translated_city, "days": "7"}

    headers = {
        "X-RapidAPI-Key": "9566aeebb1msh9e2d272ab0de5aep1a68c8jsn317fadb5dd11",
        "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    location_name = data['location']['name']
    localtime = datetime.now()
    current_temp = data['current']['temp_c']
    current_condition = translate_weather_description((data['current']['condition']['text']).lower())
    current_wind_speed = round(kph_to_mps(data['current']['wind_kph']),2)
    current_wind_dir = data['current']['wind_dir']
    current_pressure = data['current']['pressure_mb']
    current_uv = data['current']['uv']

    forecast_days = []
    for day_data in data['forecast']['forecastday']:
        date = datetime.strptime(day_data['date'], '%Y-%m-%d')
        day_name = translate_day(date.strftime('%A'))
        max_temp = day_data['day']['maxtemp_c']
        min_temp = day_data['day']['mintemp_c']
        morning_temp = day_data['hour'][6]['temp_c']
        day_temp = day_data['hour'][12]['temp_c']
        evening_temp = day_data['hour'][18]['temp_c']
        chance_of_rain = day_data['day']['daily_chance_of_rain']
        day_condition = translate_weather_description((day_data['day']['condition']['text']).lower())
        astro_data = day_data['astro']

        forecast_days.append({
            'date': date,
            'day_name': day_name,
            'max_temp': max_temp,
            'min_temp': min_temp,
            'morning_temp': morning_temp,
            'day_temp': day_temp,
            'evening_temp': evening_temp,
            'chance_of_rain': chance_of_rain,
            'day_condition': day_condition,
            'astro': astro_data
        })

    response_data = {
        'location_name': location_name,
        'localtime': localtime,
        'current_temp': current_temp,
        'current_condition': current_condition,
        'current_wind_speed': current_wind_speed,
        'current_wind_dir': current_wind_dir,
        'current_pressure': current_pressure,
        'current_uv': current_uv,
        'forecast_days': forecast_days,
        'section': 'weather',
    }
    return render(request, 'weather_api.html', response_data)


def translate_weather_description(description):
    translations = {
        'sunny': 'солнечно',
        'clear sky': 'ясное небо',
        'few clouds': 'небольшая облачность',
        'partly cloudy': 'небольшая облачность',
        'scattered clouds': 'рассеянные облака',
        'broken clouds': 'облачно с прояснениями',
        'overcast clouds': 'пасмурно',
        'shower rain': 'небольшой дождь',
        'patchy rain nearby': 'местами дождь',
        'rain': 'дождь',
        'light rain': 'легкий дождь',
        'moderate rain': 'умеренный дождь',
        'heavy intensity rain': 'сильный дождь',
        'thunderstorm': 'гроза',
        'moderate or heavy rain with thunder': 'умеренный или сильный дождь с грозой',
        'patchy light rain with thunder': 'Кратковременный мелкий дождь с грозой',
        'snow': 'снег',
        'mist': 'туман',

    }
    return (translations.get(description, description)).capitalize()


def translate_day(day):
    days = {
        'Monday': 'Понедельник',
        'Tuesday': 'Вторник',
        'Wednesday': 'Среда',
        'Thursday': 'Четверг',
        'Friday': 'Пятница',
        'Saturday': 'Суббота',
        'Sunday': 'Воскресенье',
    }
    return days.get(day, day)

def translate_city_name(city_name):
    CITY_TRANSLATIONS = {
        'Moscow': 'Москва',
        'Saint Petersburg': 'Санкт-Петербург',
        'Novosibirsk': 'Новосибирск',
        'Yekaterinburg': 'Екатеринбург',
        'Nizhny Novgorod': 'Нижний Новгород',
        'Kazan': 'Казань',
        'Chelyabinsk': 'Челябинск',
        'Omsk': 'Омск',
        'Samara': 'Самара',
        'Rostov-on-Don': 'Ростов-на-Дону',
        'Ufa': 'Уфа',
        'Krasnoyarsk': 'Красноярск',
        'Perm': 'Пермь',
        'Voronezh': 'Воронеж',
        'Volgograd': 'Волгоград',
        'Saratov': 'Саратов',
        'Krasnodar': 'Краснодар',
        'Tolyatti': 'Тольятти',
        'Izhevsk': 'Ижевск',
        'Ulyanovsk': 'Ульяновск',
        'Barnaul': 'Барнаул',
        'Vladivostok': 'Владивосток',
        'Yaroslavl': 'Ярославль',
        'Irkutsk': 'Иркутск',
        'Tyumen': 'Тюмень',
        'Khabarovsk': 'Хабаровск',
        'Makhachkala': 'Махачкала',
        'Orenburg': 'Оренбург',
        'Novokuznetsk': 'Новокузнецк',
        'Tomsk': 'Томск',
        'Kemerovo': 'Кемерово',
        'Astrakhan': 'Астрахань',
        'Kirov': 'Киров',
        'Penza': 'Пенза',
        'Lipetsk': 'Липецк',
        'Cheboksary': 'Чебоксары',
        'Tula': 'Тула',
        'Kaliningrad': 'Калининград',
        'Balashikha': 'Балашиха',
        'Kursk': 'Курск',
        'Sevastopol': 'Севастополь',
        'Sochi': 'Сочи',
        'Arkhangelsk': 'Архангельск',
        'Stavropol': 'Ставрополь',
        'Smolensk': 'Смоленск',
        'Kurgan': 'Курган',
        'Surgut': 'Сургут',
    }
    return CITY_TRANSLATIONS.get(city_name,city_name)

# def weather(request,city_name='Moscow'):
#     # profile = get_object_or_404(Profile, user=request.user)
#     profile = Profile.objects.get(user=request.user)
#     if profile.city:
#         city_name = profile.city
#     else:
#         city_name = 'Moscow'
#     # translated_city = translate_city_name(city)
#     try:
#         data = get_weather(city_name)
#         weather_obj,created = Weather.objects.get_or_create(city=city_name)
#         # weather_data_struct = json.dumps(get_weather(city), indent=2)
#         # temperature = data['main']['temp']
#         if created:
#             weather_obj.morning_weather = data['morning_weather']
#             weather_obj.day_weather = data['day_weather']
#             weather_obj.evening_weather = data['evening_weather']
#             weather_obj.current_weather = data['current_weather']
#             weather_obj.save()
#
#         # responce_data = {
#         #     'temperature': round(temperature),
#         #     'city': city_name,
#         #     'description': translate_weather_description(data['weather'][0]['description']),
#         #     'section':'weather',
#         # }
#         responce_data = {
#             'morning_weather': weather_obj.morning_weather,
#             'day_weather': weather_obj.day_weather,
#             'evening_weather': weather_obj.evening_weather,
#             'current_weather': weather_obj.current_weather,
#             'section': 'weather',
#         }
#     except KeyError as e:
#         error_message = f'KeyError: {e}'
#         return  HttpResponseServerError(error_message)
#     return render(request, 'weather_api.html', responce_data)
