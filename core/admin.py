from django.contrib import admin

from core.models import Topic, Post, Author


class PostInline(admin.TabularInline):
    model = Post
    extra = 0


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    inlines = [PostInline]


class TopicAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'topic', 'author', 'pub_date')
    list_filter = ('topic', 'author')
    search_fields = ('title', 'content')
    raw_id_fields = ('author',)
    autocomplete_fields = ('topic',)
    date_hierarchy = "pub_date"


admin.site.register(Topic, TopicAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Post, PostAdmin)
