from django_filters import rest_framework as filters

from reviews.models import Title


class CustomTitleFilter(filters.FilterSet):
    category = filters.CharFilter(
        field_name='category__slug', lookup_expr='icontains'
    )
    genre = filters.CharFilter(
        field_name='genre__slug', lookup_expr='icontains'
    )
    name = filters.CharFilter(
        field_name='name', lookup_expr='contains'
    )

    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year')
