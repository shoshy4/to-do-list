from django_filters import rest_framework as filters
from .models import Task


class TaskFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    description = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'created_date']