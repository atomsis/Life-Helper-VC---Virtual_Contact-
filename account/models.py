from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from ipware import get_client_ip
from django.contrib.auth.models import AbstractUser
import requests
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/',
                              blank=True)
    city = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f'Profile of {self.user.username}'

    def save(self, *args, **kwargs):
        if not self.city:
            ip = kwargs.pop('ip', None)
            if ip:
                city = self.get_city_from_ip(ip)
                self.city = city
        super().save(*args, **kwargs)

    def get_city_from_ip(self, ip):
        try:
            # Здесь используется стороннее API для определения города по IP.
            # Замените 'your_api_key' на реальный ключ API и 'api_endpoint' на URL API.
            api_key = '169c08615dd840b9b2e49662b11071c0'
            api_endpoint = f'https://api.ipgeolocation.io/ipgeo?apiKey={api_key}&ip={ip}'

            response = requests.get(api_endpoint)
            if response.status_code == 200:
                data = response.json()
                city = data.get('city', 'Unknown')
                return city
            else:
                print("Failed to fetch data from API")
                return "Unknown"
        except Exception as e:
            print("Error:", e)
            return "Unknown"

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
