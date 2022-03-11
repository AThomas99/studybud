from dataclasses import field
from pyexpat import model
from django.forms import ModelForm
from .models import Room
from django.contrib.auth.models import User

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__' #['name', 'body']
        exclude = ['host', 'participants', ] # Exclude host and participants while creating a room


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', ]