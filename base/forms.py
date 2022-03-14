from dataclasses import field
from pyexpat import model
from django.forms import ModelForm
from .models import Room, User
from django.contrib.auth.forms import UserCreationForm # Django user creation form


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2',]


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__' #['name', 'body']
        exclude = ['host', 'participants', ] # Exclude host and participants while creating a room


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'bio', ]