from django.contrib import admin
from .models import Category, Blog, User


admin.site.register(Category)
admin.site.register(Blog)
admin.site.register(User)
