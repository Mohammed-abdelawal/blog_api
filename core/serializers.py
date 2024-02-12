from typing import List

from rest_framework import serializers

from core.models import Topic, Post, Author


class TopicSerializer(serializers.ModelSerializer):
    """
    Serializer for Topic object.
    """

    class Meta:
        model = Topic
        fields = ('id', 'name')
        read_only_fields = ('id',)


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for Author Object.

    Methods:
        get_posts: Retrieves all posts associated with the author.
    """

    class Meta:
        model = Author
        fields = ('id', 'name', 'bio',)
        read_only_fields = ('id', 'posts')

    def get_posts(self, instance: Author) -> List[dict]:
        """
        Retrieves all posts associated with the author.

        Args:
            instance (Author): The author instance.

        Returns:
            list: List of serialized Post objects.
        """
        posts: List[Post] = Post.objects.filter(author=instance)
        serializer: PostSerializer = PostSerializer(posts, many=True)
        return serializer.data


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for Post object.
    """
    author = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all())
    topic = serializers.PrimaryKeyRelatedField(queryset=Topic.objects.all())

    pub_date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Post
        fields = ('id', "title", "topic", "content", "author", "pub_date", "author_id")
        read_only_fields = ('id',)
