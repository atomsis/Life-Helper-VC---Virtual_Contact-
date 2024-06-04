from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
###------------------------------- Admin ---------------------------------------------------------------
    path('admin/', admin.site.urls),
    # # URL для входа в административную панель
    # path('admin/login/', auth_views.LoginView.as_view(template_name='admin/login.html'), name='admin_login'),
    # # URL для выхода из административной панели
    # path('admin/logout/', auth_views.LogoutView.as_view(next_page='/'), name='admin_logout'),
###-----------------------------------------------------------------------------------------------------
    path('', include('account.urls')),
    path('weather/',include('weather_api.urls')),
    path('money_tracker/',include('money_tracker.urls',namespace='money_tracker')),
    path('chat/', include('chat.urls', namespace='chat')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
