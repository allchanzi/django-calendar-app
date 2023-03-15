from django.urls import path
from events.views import CreateEventView
from events.views import ListEventsView
from events.views import RetrieveEventView

urlpatterns = [
    path('events/', ListEventsView.as_view(), name='events'),
    path('event/', RetrieveEventView.as_view(), name='events'),
    path('create-event/', CreateEventView.as_view(), name='events'),
]
