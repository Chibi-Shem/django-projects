from django.urls import path
from . import views


app_name = 'papaya'
urlpatterns = [
    path('', views.listing, name='listing'),
    path('profile', views.profile, name='profile'),
    path('profile/create', views.profile_create, name='profile_create'),
    path('profile/edit', views.profile_edit, name='profile_edit'),
    path('profile/login', views.profile_login, name='profile_login'),
    path('profile/logout', views.profile_logout, name='profile_logout'),
    path('blogs', views.blogs, name='blogs'),
    path('blogs/create', views.blogs_create, name='blogs_create'),
    path('blogs/<int:blog_id>', views.blogs_view, name='blogs_view'),
    path('blogs/edit/<int:blog_id>', views.blogs_edit, name='blogs_edit'),
    path('blogs/delete/<int:blog_id>', views.blogs_delete, name='blogs_delete'),
]
