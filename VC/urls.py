from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('account.urls')),
    path('weather/',include('weather_api.urls')),
    path('money_tracker/',include('money_tracker.urls',namespace='money_tracker')),
    path('chat/', include('chat.urls', namespace='chat')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
