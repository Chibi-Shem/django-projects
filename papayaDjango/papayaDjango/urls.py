from django.urls import include, path
from django.contrib import admin


urlpatterns = [
    path('', include('papaya.urls')),
    path('admin/', admin.site.urls),
]
