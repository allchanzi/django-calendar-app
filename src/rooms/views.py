from rest_framework.generics import CreateAPIView
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView
from rooms.models import Room
from rooms.serializers import RoomSerializer


class ListRoomsView(ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get_queryset(self):
        query = self.request.GET
        self.queryset = Room.objects.filter(**query.dict())
        return self.queryset


class CreateRoomView(CreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class RetrieveRoomView(RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get_object(self):
        query = self.request.GET
        return self.get_queryset().get(**query.dict())
