from django.urls import path
from . import views


app_name = 'papaya'
urlpatterns = [
    path('', views.listing, name='listing'),
    path('profile/', views.registration, name='registration'),
    path('login/', views.user_login, name='login'),
    # path('myblogs/', views.myblogs, name='myblogs'),
]