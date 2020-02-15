from django.urls import path

from . import views

urlpatterns = [
    path('room/<int:id>/', views.MakeReservationView.as_view(), name='booking'),
    path('room/add/', views.CreateRoomView.as_view(), name='add_room'),
]