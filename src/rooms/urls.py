from django.urls import path
from rooms.views import CreateRoomView
from rooms.views import ListRoomsView
from rooms.views import RetrieveRoomView

urlpatterns = [
    path('rooms/', ListRoomsView.as_view(), name='rooms'),
    path('room/', RetrieveRoomView.as_view(), name='room'),
    path('create-room/', CreateRoomView.as_view(), name='room'),
]
