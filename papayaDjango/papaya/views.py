from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from .forms import UserRegistrationForm
from .forms import UserLoginForm
from django.contrib.auth import authenticate, login


def listing(request):
    return render(request, 'papaya/listing.html', {})


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('papaya:listing',))
    else:
        form = UserRegistrationForm()
    return render(request, 'papaya/profile.html', {'form':form})


def user_login(request):
    """ User login"""
    error = False
    form = UserLoginForm()
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
            else:
                error = True
    return render(request, 'papaya/login.html', {'form':form,'error':error})
