from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models
from timezone_field import TimeZoneField


class Company(models.Model):
    uuid = models.UUIDField(default=uuid4)


class User(AbstractUser):
    USERNAME_FIELD: str = 'email'
    REQUIRED_FIELDS: list = []

    email = models.EmailField(unique=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    timezone = TimeZoneField(use_pytz=False, default='UTC')
