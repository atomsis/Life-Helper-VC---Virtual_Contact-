from django.contrib import admin
from .models import Message

class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'message', 'timestamp')
    search_fields = ('sender__username', 'recipient__username', 'message')
    list_filter = ('timestamp', 'sender', 'recipient')
    actions = ['delete_selected_messages']

    def delete_selected_messages(self, request, queryset):
        queryset.delete()
    delete_selected_messages.short_description = "Удалить выбранные сообщения"

admin.site.register(Message, MessageAdmin)
