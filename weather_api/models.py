from django.db import models

class City(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Weather(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    morning_weather = models.CharField(max_length=100)
    day_weather = models.CharField(max_length=100)
    evening_weather = models.CharField(max_length=100)
    current_weather = models.CharField(max_length=100)
