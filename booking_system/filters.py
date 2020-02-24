import django_filters
from .models import Room


class RoomFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    capacity = django_filters.NumberFilter
    capacity__gt = django_filters.NumberFilter(field_name='capacity', lookup_expr='gt')
    capacity__lt = django_filters.NumberFilter(field_name='capacity', lookup_expr='lt')

    class Meta:
        model = Room
        fields = ['has_projector']
