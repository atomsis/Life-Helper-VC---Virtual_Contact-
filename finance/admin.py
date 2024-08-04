from django.contrib import admin
from .models import UserBalance

@admin.register(UserBalance)
class UseBalanceAdmin(admin.ModelAdmin):
    list_display = ['user','balance']
    list_filter = ['user']
