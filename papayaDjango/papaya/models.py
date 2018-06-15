from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser


class User(AbstractBaseUser):
    """A custom user model"""
    image = models.ImageField(
                upload_to = 'papaya/static/papaya/images',
                default = 'papaya/static/papaya/images/anon.jpeg')
    username = models.CharField(max_length=200)
    email = models.EmailField(max_length=300)
    fname = models.CharField(max_length=200)
    lname = models.CharField(max_length=200)

    USERNAME_FIELD = 'username'


class Category(models.Model):
    """A category model"""
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.category


class Blog(models.Model):
    """A blog model"""
    image = models.ImageField(upload_to = 'papaya/static/papaya/images',
                              default = 'papaya/static/papaya/images/empty.png')
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date_created = models.DateTimeField()
    date_updated = models.DateTimeField()
    content = models.TextField()

    def __str__(self):
        return self.title
