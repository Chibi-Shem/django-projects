from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegistrationForm, UserEditForm
from .forms import UserLoginForm, UserChangepassForm, BlogForm
from .models import Blog
import datetime


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
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            import pdb; pdb.set_trace()
            user = authenticate(request,
                                username=username,
                                password=password)
            login(request, user)
            return redirect(reverse('papaya:listing'))
    return render(request, 'papaya/profile_create.html', {'form':form})


def profile_edit(request):
    """Displays the user's edit page"""
    user = User.objects.get(username=request.user.username)
    form = UserEditForm(
                initial={'username':user.username, 'email':user.email,
                         'fname':user.first_name, 'lname':user.last_name,
                        })
    if request.method == 'POST':
        form = UserEditForm(request.POST)
        if form.is_valid():
            form.update()
            return redirect(reverse('papaya:profile', args=(user.id,)))
    return render(request, 'papaya/profile_edit.html', {'form':form})


def profile_changepass(request):
    """Displays the user's edit password page"""
    error = False
    user = User.objects.get(username=request.user.username)
    form = UserChangepassForm(initial={'username':user.username})
    if request.method == 'POST':
        form = UserChangepassForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password_old = form.cleaned_data['password_old']
            user = authenticate(request,
                                username=username,
                                password=password_old)
            if user is not None:
                form.update()
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(request,
                                    username=username,
                                    password=password)
                login(request, user)
                return redirect(reverse('papaya:profile', args=(user.id,)))
            else:
                error = True
    return render(request, 'papaya/profile_changepass.html',
                 {'form':form, 'error':error})


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


def profile(request, profile_id):
    """Displays the user's profile page"""
    return render(request, 'papaya/profile.html',
                  {'profile':User.objects.get(id=profile_id)})


def blogs(request):
    """Displays the user's blogs page"""
    return render(request, 'papaya/blogs.html',
                 {'blogs':Blog.objects.filter(author=request.user)})


def blogs_create(request):
    """Displays the create blogs page"""
    form = BlogForm(initial={'author':request.user,
                             'date_created':datetime.datetime.now(),
                             'date_updated':datetime.datetime.now()})
    if request.method=='POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('papaya:blogs'))
    return render(request, 'papaya/blogs_create.html',
                 {'form':form, 'blog_image':'static/papaya/images/empty.png'})


def blogs_view(request, blog_id):
    """Displays the blog's detail page"""
    blog = Blog.objects.get(id=blog_id)
    if request.method=='POST':
        if request.POST['action'] == 'edit':
            form = BlogForm(initial={'image':blog.image,
                                     'title':blog.title,
                                     'author':request.user,
                                     'date_created':blog.date_created,
                                     'date_updated':datetime.datetime.now(),
                                     'category':blog.category,
                                     'content':blog.content
                                    })
            return render(request, 'papaya/blogs_create.html',
                         {'form':form, 'blog_image':blog.image.url[7:]})
        elif request.POST['action'] == 'delete':
            blog.delete()
            return redirect(reverse('papaya:blogs'))
        elif request.POST['action'] == 'done':
            form = BlogForm(request.POST, request.FILES)
            if form.is_valid():
                blog.image = form.cleaned_data['image']
                blog.title = form.cleaned_data['title']
                blog.author = form.cleaned_data['author']
                blog.category = form.cleaned_data['category']
                blog.date_updated = form.cleaned_data['date_updated']
                blog.content = form.cleaned_data['content']
                blog.save(update_fields=['image', 'title', 'author',
                                         'category', 'date_updated',
                                         'content'])
                return redirect(reverse('papaya:blogs_view', args=(blog_id,)))
    return render(request, 'papaya/blogs_view.html',
                 {'blog':Blog.objects.get(id=blog_id),
                  'blog_image':blog.image.url[7:]})
