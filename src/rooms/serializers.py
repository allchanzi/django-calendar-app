from contrib.serializers import UserField
from django.db.models import QuerySet
from rest_framework import serializers
from rooms.models import Room


class RoomSerializer(serializers.ModelSerializer):
    manager = UserField()

    class Meta:
        model = Room
        fields = '__all__'


class RoomField(serializers.PrimaryKeyRelatedField):
    def to_representation(self, value: Room) -> dict:
        room = Room.objects.get(pk=value.pk)
        serializer = RoomSerializer(room)
        return serializer.data

    def get_queryset(self) -> QuerySet | list[Room]:
        return Room.objects.all()
