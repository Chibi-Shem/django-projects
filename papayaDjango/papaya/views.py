from django.shortcuts import render
from django.contrib.auth.models import User


def listing(request):
    return render(request,'papaya/listing.html', {})

def register(request, username, password):
    user = User.objects.create_user(username, '', password)