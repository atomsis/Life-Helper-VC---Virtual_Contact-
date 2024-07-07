from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'message', 'timestamp')
    search_fields = ('sender__username', 'recipient__username', 'message')
    list_filter = ('timestamp',)
