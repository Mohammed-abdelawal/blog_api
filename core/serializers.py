from rest_framework import serializers

from core.models import Topic, Post, Author


class TopicSerializer(serializers.ModelSerializer):
    """Serializer for Topic object"""

    class Meta:
        model = Topic
        fields = ('id', 'name')
        read_only_fields = ('id',)


class AuthorSerializer(serializers.ModelSerializer):
    """Serializer for Author Object"""

    class Meta:
        model = Author
        fields = ('id',
                  'name',
                  'bio',
                  "posts",
                  )
        read_only_fields = ('id', "posts")

    def get_posts(self, instance: Author):
        posts = Post.objects.filter(author=instance)
        serializer = PostSerializer(posts, many=True)
        return serializer.data


class PostSerializer(serializers.ModelSerializer):
    """Serializer for Post object"""

    author = AuthorSerializer(many=False, read_only=True)
    topic = TopicSerializer()

    class Meta:
        model = Post
        fields = ('id', 'name', "title", "topic", "content", "author", "pub_date")
        read_only_fields = ('id',)
