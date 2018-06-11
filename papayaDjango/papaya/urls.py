from django.urls import path
from . import views


app_name = 'papaya'
urlpatterns = [
    path('', views.listing, name='listing'),
    path('<str:username>/', views.register, name='register'),
]