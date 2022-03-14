from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages # using flash messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import UserCreationForm # Django user creation form
from django.db.models import Q

from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, MyUserCreationForm

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
        email = request.POST.get('email').lower() # update - make all username entered be lowercase
        password = request.POST.get('password')

        # check if the user exists, if dont output a flash message
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist') # use flash error message

        # Get user object and authenticate based on username and password
        user = authenticate(request, email=email, password=password)

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
    form = MyUserCreationForm()
    
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
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
    topics = Topic.objects.all()[:5]

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
    topics = Topic.objects.all()
    if request.method == 'POST': # check if it is post method
        topic_name = request.POST.get('topic') # fetch topic name from topic input on room_form.html
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),
        )

        # form = RoomForm(request.POST) # add data to the form
        # if form.is_valid(): # check if it is valid
        #     room = form.save(commit=False)
        #     room.host = request.user # The logged-in user is the one who should create the room
        #     form.save() # save it 
        return redirect('home') # redirect to homepage
    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)


# Function to update room
@login_required(login_url='login') 
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room) # adding instance to match the room
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic') # fetch topic name from topic input on room_form.html
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        # form = RoomForm(request.POST, instance=room) # targeting specific data of room instance
        # if form.is_valid():
        #     form.save()
        return redirect('home')
    context = {
        'form': form,
        'room': room,
        'topics': topics
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


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)


    context = {'form': form}
    return render(request, 'base/update_user.html', context)

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else '' # create a variable to get whatever we pass on the URL
    topics  = Room.objects.filter(
        # Q(topic__name__icontains=q) | # & - and | - or
        Q(name__icontains=q)
        # Q(description__icontains=q)
    )

    context = {'topics': topics}
    return render(request, 'base/topics.html', context)


def activityPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    room_comments = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {'room_comments': room_comments}
    return render(request, 'base/activity.html', context)