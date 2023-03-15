from contrib.models import User
from django.db import models
from rooms.models import Room


class Event(models.Model):
    owner = models.ForeignKey(
        User, related_name='owned_events', on_delete=models.PROTECT,
    )
    name = models.CharField(max_length=255)
    # possible to use JSON Field or TextField here, based on additional details
    agenda = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    participants = models.ManyToManyField(User, related_name='events')
    location = models.ForeignKey(
        Room, null=True, blank=True, on_delete=models.SET_NULL,
    )  # Based on further details could make sense to use CASCADE
