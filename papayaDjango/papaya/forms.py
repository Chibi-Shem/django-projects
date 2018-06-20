from django import forms
from django.forms import Form, ModelForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Blog, User

class UserRegistrationForm(ModelForm):
    """Registration form for users"""
    class Meta:
        model = User
        fields = ['username', 'password', 'password2']

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
        user = User.objects.create(username = username)
        user.set_password(password)
        user.save()


class UserEditForm(ModelForm):
    """Profile editing form for users"""
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'image']

    email = forms.EmailField(widget=forms.EmailInput, required=False,
                             label="Email:", max_length=200)
    first_name = forms.CharField(widget=forms.TextInput, required=False,
                            label="First name:", max_length=100)
    last_name = forms.CharField(widget=forms.TextInput, required=False,
                            label="Last name:", max_length=100)
    image = forms.ImageField(widget=forms.FileInput, required=False,
                            label="Image:")

    email.widget.attrs.update({'class':'form-control',
                               'placeholder':'Enter email'})
    first_name.widget.attrs.update({'class':'form-control',
                               'placeholder':'Enter first name'})
    last_name.widget.attrs.update({'class':'form-control',
                               'placeholder':'Enter last name'})
    image.widget.attrs.update({'class':'form-control'})


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


class UserChangepassForm(ModelForm):
    """Change password form for users"""
    class Meta:
        model = User
        fields = ['password']

    password = forms.CharField(widget=forms.PasswordInput,
                               label="Current Password:", max_length=100)
    password_new = forms.CharField(widget=forms.PasswordInput,
                               label="New Password:", max_length=100)
    password_confirm = forms.CharField(widget=forms.PasswordInput,
                               label="Password:", max_length=100)

    password.widget.attrs.update({'class':'form-control',
                                  'placeholder':'Enter current password'})
    password_new.widget.attrs.update({'class':'form-control',
                                  'placeholder':'Enter new password'})
    password_confirm.widget.attrs.update({'class':'form-control',
                                  'placeholder':'Confirm new password'})

    def clean_password_confirm(self):
        password_new = self.cleaned_data['password_new']
        password_confirm = self.cleaned_data['password_confirm']
        if password_new != password_confirm:
            raise forms.ValidationError("Password mismatch")
        return password_new

    def update(self, username):
        user = User.objects.get(username=username)
        user.set_password(self.cleaned_data['password_new'])
        user.save()


class BlogForm(ModelForm):
    """Blog form for users"""
    class Meta:
        model = Blog
        fields = ['image', 'title', 'author', 'category', 'content']

    image = forms.ImageField(widget=forms.FileInput, required=False,
                            label="Image:")
