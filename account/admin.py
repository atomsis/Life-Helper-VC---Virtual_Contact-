from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user','email','date_of_birth', 'city', 'get_photo_display']

    def get_photo_display(self, obj):
        if obj.photo:
            return '<img src="%s" width="50" />' % obj.photo.url
        else:
            return 'No photo'

    get_photo_display.allow_tags = True
    get_photo_display.short_description = 'Photo'

    def email(self, obj):
        return obj.user.email

    email.short_description = 'Email'
    email.admin_order_field = 'user__email'