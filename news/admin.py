from django.contrib import admin
from .models import Author, Post, Category, Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ('typePost', 'namePost', 'textPost')
    list_filter = ('typePost',)
    search_fields = ('typePost', 'namePost', 'textPost')

admin.site.register(Author)
admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Comment)
