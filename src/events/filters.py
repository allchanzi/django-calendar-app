import datetime

from django.db.models import QuerySet
from django_filters import DateFilter
from django_filters import FilterSet
from django_filters import NumberFilter
from events.models import Event


class EventFilter(FilterSet):
    day = DateFilter(method='filter_day')
    location_id = NumberFilter(field_name='location__id')

    @staticmethod
    def filter_day(queryset: QuerySet, _, value: datetime.date, *args, **kwargs):
        return queryset.filter(start_time__date__lte=value, end_time__date__gte=value)

    class Meta:
        model = Event
        fields = '__all__'
