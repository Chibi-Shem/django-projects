from django.urls import include, path
from django.contrib import admin

urlpatterns = [
    path('papaya/', include('papaya.urls')),
    path('admin/', admin.site.urls),
]
