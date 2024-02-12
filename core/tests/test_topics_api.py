from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Topic
from core.serializers import TopicSerializer
from core.tests.factories import TopicFactory, UserFactory

TOPICS_URL = '/api/v1/topics/'


class PublicTopicApiTest(TestCase):
    """Test Public Topic API"""

    def setUp(self):
        self.client = APIClient()
        self.topic = TopicFactory()

    def test_login_required(self):
        """Test login required to view topics"""
        url = f"{TOPICS_URL}{self.topic.id}/"

        res = self.client.post(url, data={})
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_list(self):
        res = self.client.get(TOPICS_URL)

        # Serialize the topics
        topics = Topic.objects.all()
        serializer = TopicSerializer(topics, many=True)

        self.assertEqual(res.data, serializer.data)

    def test_can_get(self):
        url = f"{TOPICS_URL}{self.topic.id}/"

        res = self.client.get(url)

        # Serialize the topics
        serializer = TopicSerializer(self.topic)

        self.assertEqual(res.data, serializer.data)


class PrivateTopicApiTest(TestCase):
    """Test the authenticated user topics API"""

    def setUp(self):
        self.user = UserFactory()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_topics(self):
        """Test retrieving topics"""
        TopicFactory.create_batch(2)

        res = self.client.get(TOPICS_URL)

        topics = Topic.objects.all()
        serializer = TopicSerializer(topics, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_topic_successful(self):
        """Test creating a new topic"""
        payload = {'name': 'New Topic'}
        res = self.client.post(TOPICS_URL, payload)

        exists = Topic.objects.filter(name=payload['name']).exists()
        self.assertTrue(exists)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_topic_invalid(self):
        """Test creating a new topic with invalid data"""
        payload = {'name': ''}
        res = self.client.post(TOPICS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
