import imp
from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Room, Topic
from .forms import RoomForm

# rooms = [
#     {'id': 1, 'name': 'Lets learn python'},
#     {'id': 2, 'name': 'Lets learn HTML'},
#     {'id': 3, 'name': 'Lets learn CSS'},
# ]

# Create your views here.
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else '' # create a variable to get whatever we pass on the URL
    
    rooms  = Room.objects.filter(
        Q(topic__name__icontains=q) | # & - and | - or
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()

    room_count = rooms.count()

    context = {
        'rooms': rooms,
        'topics': topics,
        'room_count': room_count,
    }
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'room': room}
    return render(request, 'base/room.html', context)


# Function to create room
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST': # check if it is post method
        form = RoomForm(request.POST) # add data to the form
        if form.is_valid(): # check if it is valid
            form.save() # save it 
            return redirect('home') # redirect to homepage
    context = {'form': form}
    return render(request, 'base/room_form.html', context)


# Function to update room
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room) # adding instance to match the room

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room) # targeting specific data of room instance
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {
        'form': form,
        'room': room,
    }
    return render(request, 'base/room_form.html', context)


# Fundtion to delete room
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.method == 'POST':
        room.delete() # delete the room on the database
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})