from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('user-profile/<str:pk>/', views.userProfile, name='user-profile'),
    path('update-user/', views.updateUser, name='update-user'),

    path('', views.home, name="home"),
    path('room/<str:pk>/', views.room, name="room"),
    path('topics/', views.topicsPage, name="topics"),
    path('activities/', views.activityPage, name="activities"),

    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
    path('delete-comment/<str:pk>/', views.deleteComment, name="delete-comment"),
]
