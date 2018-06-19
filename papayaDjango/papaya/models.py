from django.db import models
from django.contrib.auth.models import User


class PapayaUser(models.Model):
    """A custom user model"""
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    image = models.ImageField(upload_to = 'papaya/images')
    
    def __str__(self):
        return self.user.username


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
    date_created = models.TimeField(auto_now_add = True)
    date_updated = models.TimeField(auto_now = True)
    content = models.TextField()

    def __str__(self):
        return self.title
