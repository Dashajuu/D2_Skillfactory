from django import forms
from .models import Post, Category


class PostForm(forms.ModelForm):
    namePost = forms.CharField(label='Название поста')
    textPost = forms.CharField(label='Основное содержание', min_length=20, widget=forms.Textarea)

    class Meta:
        model = Post
        fields = [
            'namePost',
            'textPost',
            'category',
            'author',
        ]
