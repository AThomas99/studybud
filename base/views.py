from django.shortcuts import render, redirect
from .models import Room
from .forms import RoomForm

# rooms = [
#     {'id': 1, 'name': 'Lets learn python'},
#     {'id': 2, 'name': 'Lets learn HTML'},
#     {'id': 3, 'name': 'Lets learn CSS'},
# ]

# Create your views here.
def home(request):
    rooms  = Room.objects.all()
    context = {'rooms': rooms}
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