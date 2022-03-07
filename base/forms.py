from dataclasses import field
from django.forms import ModelForm
from .models import Room

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__' #['name', 'body']
        exclude = ['host', 'participants', ] # Exclude host and participants while creating a room