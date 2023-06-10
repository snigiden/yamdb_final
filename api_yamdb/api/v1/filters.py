import django_filters
from django_filters import CharFilter
from reviews.models import Title


class TitleFilter(django_filters.FilterSet):
    name = CharFilter(lookup_expr='icontains')
    genre = CharFilter(field_name='genre__slug')
    category = CharFilter(field_name='category__slug')

    class Meta:
        model = Title
        fields = ['year']
