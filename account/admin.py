from django.contrib import admin
from .models import Profile,Friendship
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


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


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Профиль'

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, )
    list_display = ('username', 'email', 'get_city')

    def get_city(self, obj):
        return obj.profile.city if hasattr(obj, 'profile') else None
    get_city.short_description = 'Город'

admin.site.unregister(User)
admin.site.register(User, UserAdmin)


admin.site.register(Friendship)