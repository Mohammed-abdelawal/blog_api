from rest_framework import permissions
from rest_framework import viewsets

from core.models import Topic, Post, Author
from core.serializers import TopicSerializer, PostSerializer, AuthorSerializer


class TopicViewSet(viewsets.ModelViewSet):
    """
    A view set for managing topics.

    This view set provides CRUD operations for topics in the blog.
    """
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class PostViewSet(viewsets.ModelViewSet):
    """
    A view set for managing posts.

    This view set provides CRUD operations for posts in the blog.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class AuthorViewSet(viewsets.ModelViewSet):
    """
    A view set for managing authors.

    This view set provides CRUD operations for authors in the blog.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
