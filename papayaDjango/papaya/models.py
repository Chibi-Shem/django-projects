from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """A custom user model"""
    image = models.ImageField(upload_to = 'papaya/images')
    
    def __str__(self):
        return self.username


class Category(models.Model):
    """A category model"""
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.category


class Blog(models.Model):
    """A blog model"""
    image = models.ImageField(upload_to = 'papaya/images')
    title = models.CharField(max_length = 200)
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    date_created = models.DateField(auto_now_add = True)
    date_updated = models.DateField(auto_now = True)
    time_created = models.TimeField(auto_now_add = True)
    time_updated = models.TimeField(auto_now = True)
    content = models.TextField()

    def __str__(self):
        return self.title
