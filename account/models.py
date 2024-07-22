from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from ipware import get_client_ip
from django.contrib.auth.models import AbstractUser
import requests
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Friendship(models.Model):
    from_user = models.ForeignKey(User, related_name='friendship_from', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='friendship_to', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.from_user.username} -> {self.to_user.username}'

class Profile(models.Model):
    objects = None
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/',
                              blank=True)
    city = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)


    def add_friend(self, friend_profile):
        Friendship.objects.get_or_create(from_user=self.user, to_user=friend_profile.user)
        Friendship.objects.get_or_create(from_user=friend_profile.user, to_user=self.user)

    def remove_friend(self, friend_profile):
        Friendship.objects.filter(from_user=self.user, to_user=friend_profile.user).delete()
        Friendship.objects.filter(from_user=friend_profile.user, to_user=self.user).delete()

    def get_friends(self):
        return User.objects.filter(
            id__in=Friendship.objects.filter(from_user=self.user).values_list('to_user_id', flat=True)
        )

    def __str__(self):
        return f'Profile of {self.user.username}'
