from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from django.conf import settings

urlpatterns = [
    path('profile/',include('profile_user.urls')),
    path('admin/', admin.site.urls),
    path('',include('movies.urls'))

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA,document_root = settings.MEDIA_ROOT)