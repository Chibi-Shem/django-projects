from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegistrationForm, UserLoginForm, BlogForm
from .models import Blog


def listing(request):
    """Displays the list of all blogs"""
    blogs = Blog.objects.all()
    if request.method == 'POST':
        blogs = Blog.objects.filter(title__icontains=request.POST['search'])
    return render(request, 'papaya/listing.html', {'blogs':blogs})


def profile_create(request):
    """Displays the user's registration page"""
    form = UserRegistrationForm()
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect(reverse('papaya:listing'))
    return render(request, 'papaya/profile_create.html', {'form':form})


def profile_edit(request):
    """Displays the blog's edit page"""
    form = UserRegistrationForm(
                initial={'username':request.user.username,
                         'email':request.user.email,
                         'fname':request.user.first_name,
                         'lname':request.user.last_name,
                        })
    if request.method=='POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            request.user.username = form.cleaned_data['username']
            request.user.password = form.cleaned_data['password']
            request.user.email = form.cleaned_data['email']
            request.user.first_name = form.cleaned_data['fname']
            request.user.last_name = form.cleaned_data['lname']
            request.user.save(update_fields=['username', 'password',
                                             'email', 'first_name', 'last_name'])
            return redirect(reverse('papaya:profile'))
    return render(request, 'papaya/profile_create.html', {'form':form})


def profile_login(request):
    """Displays the user's login page"""
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
                return redirect(reverse('papaya:listing'))
            else:
                error = True
    return render(request, 'papaya/profile_login.html',
                 {'form':form,'error':error})


def profile_logout(request):
    """Logs out a user"""
    logout(request)
    return redirect(reverse('papaya:listing'))


def profile(request):
    """Displays the user's profile page"""
    return render(request, 'papaya/profile.html', {})


def blogs(request):
    """Displays the user's blogs page"""
    return render(request, 'papaya/blogs.html',
                 {'blogs':Blog.objects.filter(author=request.user)})


def blogs_create(request):
    """Displays the create blogs page"""
    form = BlogForm(initial={'author':request.user})
    if request.method=='POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('papaya:blogs'))
    return render(request, 'papaya/blogs_create.html', {'form':form})


def blogs_view(request, blog_id):
    """Displays the blog's detail page"""
    return render(request, 'papaya/blogs_view.html',
                 {'blog':Blog.objects.get(id=blog_id)})


def blogs_edit(request, blog_id):
    """Displays the blog's edit page"""
    blog = Blog.objects.get(id=blog_id)
    form = BlogForm(initial={'title':blog.title, 'author':request.user,
                             'category':blog.category, 'content':blog.content
                            })
    if request.method=='POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            blog.title = form.cleaned_data['title']
            blog.author = form.cleaned_data['author']
            blog.category = form.cleaned_data['category']
            blog.content = form.cleaned_data['content']
            blog.save(update_fields=['title', 'author',
                                     'category', 'content'])
            return redirect(reverse('papaya:blogs'))
    return render(request, 'papaya/blogs_create.html', {'form':form})


def blogs_delete(request, blog_id):
    """Deletes the current blog"""
    blog = Blog.objects.get(id=blog_id)
    blog.delete()
    return redirect(reverse('papaya:blogs'))
