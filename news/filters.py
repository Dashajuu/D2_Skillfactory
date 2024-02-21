from django_filters import FilterSet, ModelMultipleChoiceFilter, CharFilter, DateTimeFilter
from django import forms

from .models import Post, Category


class PostFilter(FilterSet):
    category = ModelMultipleChoiceFilter(
        field_name='postcategory__category',
        queryset=Category.objects.all(),
        label='Категории',
        widget=forms.CheckboxSelectMultiple()
    )
    namePost = CharFilter(lookup_expr='icontains', label='Название')
    dataPost = DateTimeFilter(
        field_name='dataPost',
        lookup_expr='gte',
        label='Дата',
        widget=forms.DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
    )

    class Meta:
        model = Post
        fields = [
            'namePost',
            'dataPost',
        ]
