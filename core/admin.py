from django.contrib import admin

from core.models import Topic, Author, Post

admin.site.register(Topic)
admin.site.register(Author)
admin.site.register(Post)
