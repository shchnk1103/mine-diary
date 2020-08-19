from blog.models import Post
from django_filters import rest_framework


class PostFilter(rest_framework.FilterSet):
    created_year = rest_framework.NumberFilter(
        field_name='created_time', lookup_expr='year'
    )
    created_month = rest_framework.NumberFilter(
        field_name='created_time', lookup_expr='month'
    )

    class Meta:
        model = Post
        fields = [
            'categories',
            'created_year',
            'created_month'
        ]
