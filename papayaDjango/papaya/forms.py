from django import forms
from django.contrib.auth.models import User
from django.forms import Form, ModelForm
from .models import Blog

class UserRegistrationForm(Form):
    """Registration form for users"""
    username = forms.CharField(widget=forms.TextInput(),
                               label="Username:", max_length=100)
    password = forms.CharField(widget=forms.PasswordInput,
                               label="Password:", max_length=100)
    password2 = forms.CharField(widget=forms.PasswordInput,
                                label="", max_length=100)

    username.widget.attrs.update({'class':'form-control',
                                  'placeholder':'Enter username'})
    password.widget.attrs.update({'class':'form-control',
                                  'placeholder':'Enter password'})
    password2.widget.attrs.update({'class':'form-control',
                                   'placeholder':'Confirm password'})

    def clean_password2(self):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError("Password mismatch")
        return password

    def clean_username(self):
        username = self.cleaned_data['username']
        exists = User.objects.filter(username=username)
        if exists:
            raise forms.ValidationError("Username already exists")
        return username

    def save(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = User.objects.create_user(username, password)
        return user


class UserEditForm(Form):
    """Profile editing form for users"""
    username = forms.CharField(widget=forms.TextInput(),
                               label="Username:", max_length=100)
    email = forms.EmailField(widget=forms.EmailInput, required=False,
                             label="Email:", max_length=200)
    fname = forms.CharField(widget=forms.TextInput, required=False,
                            label="First name:", max_length=100)
    lname = forms.CharField(widget=forms.TextInput, required=False,
                            label="Last name:", max_length=100)

    username.widget.attrs.update({'class':'form-control',
                                  'placeholder':'Enter username'})
    email.widget.attrs.update({'class':'form-control',
                               'placeholder':'Enter email'})
    fname.widget.attrs.update({'class':'form-control',
                               'placeholder':'Enter first name'})
    lname.widget.attrs.update({'class':'form-control',
                               'placeholder':'Enter last name'})

    def update(self):
        user = User.objects.get(username=self.cleaned_data['username'])
        user.email = self.cleaned_data['email'].lower()
        user.first_name = self.cleaned_data['fname']
        user.last_name = self.cleaned_data['lname']
        user.save()
        return user


class UserPasswordForm(Form):
    """Profile editing form for users"""
    username = forms.CharField(widget=forms.TextInput(),
                               label="Username:", max_length=100)
    password = forms.CharField(widget=forms.PasswordInput,
                               label="Password:", max_length=100)
    password2 = forms.CharField(widget=forms.PasswordInput,
                                label="", max_length=100)
    email = forms.EmailField(widget=forms.EmailInput, required=False,
                             label="Email:", max_length=200)
    fname = forms.CharField(widget=forms.TextInput, required=False,
                            label="First name:", max_length=100)
    lname = forms.CharField(widget=forms.TextInput, required=False,
                            label="Last name:", max_length=100)

    username.widget.attrs.update({'class':'form-control',
                                  'placeholder':'Enter username'})
    password.widget.attrs.update({'class':'form-control',
                                  'placeholder':'Enter password'})
    password2.widget.attrs.update({'class':'form-control',
                                   'placeholder':'Confirm password'})
    email.widget.attrs.update({'class':'form-control',
                               'placeholder':'Enter email'})
    fname.widget.attrs.update({'class':'form-control',
                               'placeholder':'Enter first name'})
    lname.widget.attrs.update({'class':'form-control',
                               'placeholder':'Enter last name'})

    def clean_password2(self):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError("Password mismatch")
        return password

    def update(self):
        user = User.objects.get(username=self.cleaned_data['username'])
        user.set_password(self.cleaned_data['password'])
        user.first_name = self.cleaned_data['fname']
        user.last_name = self.cleaned_data['lname']
        user.save()
        return user


class UserLoginForm(Form):
    """Login form for users"""
    username = forms.CharField(widget=forms.TextInput(),
                               label="Username:", max_length=100)
    password = forms.CharField(widget=forms.PasswordInput,
                               label="Password:", max_length=100)

    username.widget.attrs.update({'class':'form-control',
                                  'placeholder':'Enter username'})
    password.widget.attrs.update({'class':'form-control',
                                  'placeholder':'Enter password'})

class BlogForm(ModelForm):
    """Blog form for users"""

    class Meta:
        model = Blog
        fields = ['title', 'author', 'category',
                  'date_created', 'date_updated',
                  'content']
