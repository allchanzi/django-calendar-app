from typing import Callable

from django.utils import timezone
from rest_framework.response import Response


class TimezoneMiddleware:
    def __init__(self, get_response: Callable):
        self.get_response = get_response

    def __call__(self, request) -> Response:
        tzname = request.META.get('django_timezone') or (
            request.user.timezone if not request.user.is_anonymous else None
        )
        timezone.activate(tzname) if tzname is not None else timezone.deactivate()
        return self.get_response(request)
