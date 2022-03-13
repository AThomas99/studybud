from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes),
    path('rooms/', views.getRooms), # all rooms
    path('rooms/<int:pk>/', views.getRoom), # single room
]
