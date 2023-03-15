from contrib.serializers import UserField
from contrib.serializers import UserSerializer
from events.models import Event
from events.validators import MaxDurationValidator
from rest_framework import serializers
from rooms.serializers import RoomField


class EventSerializer(serializers.ModelSerializer):
    owner = UserField()
    participants = UserSerializer(many=True, required=False)
    location = RoomField()

    class Meta:
        model = Event
        fields = '__all__'
        validators = [MaxDurationValidator()]
