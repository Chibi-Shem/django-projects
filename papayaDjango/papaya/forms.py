from django import forms
from django.forms import Form, ModelForm
from .models import Blog, User

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
        user = User.objects.create(username = username)
        user.set_password(password)
        user.save()


class UserEditForm(ModelForm):
    """Profile editing form for users"""
    class Meta:
        model = User
        fields = ['image']

    username = forms.CharField(widget=forms.TextInput(),
                               label="Username:", max_length=100)
    email = forms.EmailField(widget=forms.EmailInput, required=False,
                             label="Email:", max_length=200)
    fname = forms.CharField(widget=forms.TextInput, required=False,
                            label="First name:", max_length=100)
    lname = forms.CharField(widget=forms.TextInput, required=False,
                            label="Last name:", max_length=100)
    image = forms.ImageField(widget=forms.FileInput, required=False,
                            label="Image:")

    username.widget.attrs.update({'class':'form-control',
                                  'placeholder':'Enter username'})
    email.widget.attrs.update({'class':'form-control',
                               'placeholder':'Enter email'})
    fname.widget.attrs.update({'class':'form-control',
                               'placeholder':'Enter first name'})
    lname.widget.attrs.update({'class':'form-control',
                               'placeholder':'Enter last name'})
    image.widget.attrs.update({'class':'form-control'})

    def update(self):
        user = User.objects.get(username=self.cleaned_data['username'])
        user.email = self.cleaned_data['email'].lower()
        user.first_name = self.cleaned_data['fname']
        user.last_name = self.cleaned_data['lname']
        user.image = self.cleaned_data['image']
        user.save()


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


class UserChangepassForm(Form):
    """Change password form for users"""
    username = forms.CharField(widget=forms.TextInput(),
                               label="Username:", max_length=100)
    password_old = forms.CharField(widget=forms.PasswordInput,
                               label="Current Password:", max_length=100)
    password = forms.CharField(widget=forms.PasswordInput,
                               label="New Password:", max_length=100)
    password2 = forms.CharField(widget=forms.PasswordInput,
                               label="Password:", max_length=100)

    username.widget.attrs.update({'class':'form-control',
                                  'placeholder':'Enter username'})
    password_old.widget.attrs.update({'class':'form-control',
                                  'placeholder':'Enter current password'})
    password.widget.attrs.update({'class':'form-control',
                                  'placeholder':'Enter new password'})
    password2.widget.attrs.update({'class':'form-control',
                                  'placeholder':'Confirm new password'})

    def clean_password2(self):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError("Password mismatch")
        return password

    def update(self):
        user = User.objects.get(username=self.cleaned_data['username'])
        user.set_password(self.cleaned_data['password'])
        user.save()


class BlogForm(ModelForm):
    """Blog form for users"""

    class Meta:
        model = Blog
        fields = ['image', 'title', 'author', 'category', 'content']

    image = forms.ImageField(widget=forms.FileInput, required=False,
                            label="Image:")

    def update(self, blog_id):
        blog = Blog.objects.get(id=blog_id)
        blog.image = self.cleaned_data['image']
        blog.title = self.cleaned_data['title']
        blog.author = self.cleaned_data['author']
        blog.category = self.cleaned_data['category']
        blog.content = self.cleaned_data['content']
        blog.save()
