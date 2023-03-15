from django.db.models import Q
from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from events.filters import EventFilter
from events.models import Event
from events.serializers import EventSerializer
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response


class ListEventsView(ListAPIView):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_class = EventFilter
    search_fields = ['agenda', 'name']

    def get_queryset(self) -> QuerySet | list[Event]:
        user = self.request.user
        return Event.objects.filter(Q(participants=user) | Q(owner=user) | Q(location__manager=user))


class RetrieveEventView(RetrieveAPIView):
    serializer_class = EventSerializer

    def get_object(self) -> Event:
        user = self.request.user
        query = self.request.GET
        queryset = Event.objects.filter(Q(participants=user) | Q(owner=user) | Q(location__manager=user))
        return queryset.get(**query.dict())


class CreateEventView(CreateAPIView):
    serializer_class = EventSerializer

    def create(self, request: Request, *args, **kwargs) -> Response:
        data = request.data.dict()
        data['owner'] = request.user.pk
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
