from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('room/book/<int:id>/', views.MakeReservationView.as_view(), name='booking'),
    path('room/add/', views.CreateRoomView.as_view(), name='add_room'),
    path('room/<int:id>/', views.RoomDetailsView.as_view(), name='room_details'),
    path('room/update/<int:id>/', views.UpdateRoomView.as_view(), name='room_update'),
    path('room/list/', views.AllRoomsView.as_view(), name='rooms_list'),
    path('room/delete/<int:id>', views.DeleteRoomView.as_view(), name='delete_room'),
    path('room/deleted/', views.DeletedRoomView.as_view(), name='deleted_room'),
    path('room/search/', views.SearchRoomView.as_view(), name='search_room'),
]