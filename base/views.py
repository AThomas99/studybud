from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages # using flash messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm # Django user creation form
from django.db.models import Q

from .models import Room, Topic, Message
from .forms import RoomForm

# rooms = [
#     {'id': 1, 'name': 'Lets learn python'},
#     {'id': 2, 'name': 'Lets learn HTML'},
#     {'id': 3, 'name': 'Lets learn CSS'},
# ]

# Function to login page
def loginPage(request):
    page = 'login'


    # Restrict user on login page if is already logged in
    if request.user.is_authenticated:
        return redirect('home')


    if request.method == 'POST':
        username = request.POST.get('username').lower() # update - make all username entered be lowercase
        password = request.POST.get('password')

        # check if the user exists, if dont output a flash message
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist') # use flash error message

        # Get user object and authenticate based on username and password
        user = authenticate(request, username=username, password=password)

        if user is not None: # check if there is user or no user
            login(request, user) # Login the user and add the session into the db and browser
            return redirect('home')

        else:
            messages.error(request, 'Username or password does not exist') # use flash error message
            print(user)

    context = {'page': page}
    return render(request, 'base/auth/login_register.html', context)
    
# Function to logout user
def logoutUser(request):
    logout(request)
    return redirect('home')

# Function to register user
def registerPage(request):
    form = UserCreationForm()
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) # get user credentials without commiting to the db
            user.username = user.username.lower() # make all usernames lowercase
            user.save()
            login(request, user)
            return redirect('home')

        else:
            messages.error(request, 'An error occured during registration')
            
    context = {'form': form}

    return render(request, 'base/auth/login_register.html', context)


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
    room_comments = Message.objects.filter(Q(room__topic__name__icontains=q)) # Filters and search for rooms and related topics

    context = {
        'rooms': rooms,
        'topics': topics,
        'room_count': room_count,
        'room_comments': room_comments,
    }
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    comments = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    # Explanation:
    # Filter all comments that are available in a specific room
    # The 'message_set' comes from the model 'Message' which is the foreign key of model 'Room'
    
    # Create Comment Form
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body'),
        )
        room.participants.add(request.user) # Add user on participants list once a user comments on a topic
        return redirect('room', pk=room.id)
    
    context = {'room': room, 'comments': comments, 'participants':participants}
    return render(request, 'base/room.html', context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_comments = user.message_set.all()
    topics = Topic.objects.all()
    context = {
        'user': user,
        'rooms': rooms,
        'room_comments': room_comments,
        'topics': topics,
    }
    return render(request, 'base/profile.html', context)

# Function to create room
# Added a decorator to restrict unknown users from creating a room
@login_required(login_url='login') 
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
@login_required(login_url='login') 
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
@login_required(login_url='login') 
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.method == 'POST':
        room.delete() # delete the room on the database
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})

# Fundtion to comment room
@login_required(login_url='login') 
def deleteComment(request, pk):
    comment = Message.objects.get(id=pk)

    # if request.method != comment.user:
    #     return HttpResponse("You're not allowed here")

    if request.method == 'POST':
        comment.delete() # delete the room on the database
        return redirect('home') # we will work on this URL routing later - so that it can redirect to room page
    return render(request, 'base/delete.html', {'obj': comment})