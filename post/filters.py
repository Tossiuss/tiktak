import django_filters
from .models import Posts


class PostFilter(django_filters.FilterSet):
    class Meta:
        model = Posts
        fields = ['categories']



