from contrib.models import User
from django.db import models


class Room(models.Model):
    manager = models.ForeignKey(
        User, related_name='managed_rooms', on_delete=models.PROTECT,
    )
    name = models.CharField(max_length=255)
    # TODO will be moved to contrib and properly designed for relation database
    address = models.CharField(max_length=255)
