from urllib.parse import urljoin

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Post
from core.serializers import PostSerializer
from core.tests.factories import PostFactory, UserFactory, TopicFactory, AuthorFactory

POSTS_URL = '/api/v1/posts/'


class PublicPostApiTest(TestCase):
    """Test Public Post API"""

    def setUp(self):
        self.client = APIClient()
        self.post = PostFactory(id=1)

    def test_login_required(self):
        """Test login required to view posts"""
        url = f"{POSTS_URL}{self.post.id}/"

        res = self.client.post(url, data={"name": "1"})
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_list(self):
        res = self.client.get(POSTS_URL)

        # Serialize the posts
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)

        self.assertEqual(res.data, serializer.data)

    def test_can_get(self):
        url = urljoin(POSTS_URL, "1/")
        res = self.client.get(url)

        # Serialize the post
        serializer = PostSerializer(self.post)

        self.assertEqual(res.data, serializer.data)


class PrivatePostApiTest(TestCase):
    """Test the authenticated user posts API"""

    def setUp(self):
        self.user = UserFactory()
        self.topic = TopicFactory()
        self.author = AuthorFactory()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_posts(self):
        """Test retrieving posts"""
        PostFactory.create_batch(2)

        res = self.client.get(POSTS_URL)

        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_post_successful(self):
        """Test creating a new post"""
        payload = {
            "title": "how to",
            "topic": self.topic.id,
            "content": "<h2>Hi there</h2><p>&nbsp;</p><p>ii'' teach you how to go there</p>",
            "author": self.author.id
        }
        res = self.client.post(POSTS_URL, payload)

        exists = Post.objects.filter(title=payload['title']).exists()
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(exists)

    def test_create_post_invalid(self):
        """Test creating a new post with invalid data"""
        payload = {'title': ''}
        res = self.client.post(POSTS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
