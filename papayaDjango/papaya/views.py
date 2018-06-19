from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserEditForm
from .forms import UserChangepassForm, BlogForm, UserLoginForm
from .models import Blog, PapayaUser


def listing(request):
    """Displays the list of all blogs"""
    blogs = Blog.objects.all()
    msg = ''
    if request.method == 'POST':
        blogs = Blog.objects.filter(title__icontains=request.POST['search'])
        if not blogs:
            msg = 'No results found!'
    return render(request, 'papaya/listing.html', {'blogs':blogs, 'msg':msg})


def profile_create(request):
    """Displays the user's registration page"""
    form = UserRegistrationForm()
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,
                                username=username,
                                password=password)
            login(request, user)
            return redirect(reverse('papaya:listing'))
    return render(request, 'papaya/profile_create.html', {'form':form})


def profile_edit(request):
    """Displays the user's edit page"""
    papayaUser = PapayaUser.objects.get(user=request.user)
    form = UserEditForm(
                initial={'image': papayaUser.image,
                         'username':papayaUser.user.username,
                         'email':papayaUser.user.email,
                         'fname':papayaUser.user.first_name,
                         'lname':papayaUser.user.last_name,
                        })
    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES)
        if form.is_valid():
            if not request.FILES:
                form.cleaned_data['image'] = papayaUser.image
            form.update()
            return redirect(reverse('papaya:profile',
                                args=(papayaUser.user.id,)))
    return render(request, 'papaya/profile_edit.html',
            {'form':form, 'profile_image':papayaUser.image})


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
    user = User.objects.get(id=profile_id)
    papayaUser = PapayaUser.objects.get(user=user)
    return render(request, 'papaya/profile.html', {'profile':papayaUser})


def blogs(request):
    """Displays the user's blogs page"""
    return render(request, 'papaya/blogs.html',
                 {'blogs':Blog.objects.filter(author=request.user)})


@login_required()
def blogs_create(request):
    """Displays the create blogs page"""
    form = BlogForm(initial={'author':request.user})
    if request.method=='POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('papaya:blogs'))
    return render(request, 'papaya/blogs_create.html',
                 {'form':form})


def blogs_view(request, blog_id):
    """Displays the blog's detail page"""
    try:
        blog = get_object_or_404(Blog, id=blog_id, author=request.user)
        if request.method=='POST':
            if request.POST['action'] == 'edit':
                form = BlogForm(initial={'image':blog.image,
                                         'title':blog.title,
                                         'author':request.user,
                                         'category':blog.category,
                                         'content':blog.content
                                        })
                return render(request, 'papaya/blogs_create.html',
                             {'form':form, 'blog_image':blog.image})
            elif request.POST['action'] == 'delete':
                blog.delete()
                return redirect(reverse('papaya:blogs'))
            elif request.POST['action'] == 'done':
                form = BlogForm(request.POST, request.FILES)
                if form.is_valid():
                    if not request.FILES:
                        form.cleaned_data['image'] = blog.image
                    form.update(blog_id)
                    return redirect(reverse('papaya:blogs_view',
                                    args=(blog_id,)))
    except:
        blog = get_object_or_404(Blog, id=blog_id)
    # import pdb; pdb.set_trace()
    return render(request, 'papaya/blogs_view.html',
                 {'blog':blog})
