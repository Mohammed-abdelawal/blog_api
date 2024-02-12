from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Author
from core.serializers import AuthorSerializer
from core.tests.factories import AuthorFactory, UserFactory

AUTHORS_URL = '/api/v1/authors/'


class PublicAuthorApiTest(TestCase):
    """Test Public Author API"""

    def setUp(self):
        self.client = APIClient()
        self.author = AuthorFactory(id=1)

    def test_can_list(self):
        res = self.client.get(AUTHORS_URL)

        # Serialize the authors
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_can_get(self):
        url = f"{AUTHORS_URL}{self.author.id}/"
        res = self.client.get(url)

        # Serialize the author
        serializer = AuthorSerializer(self.author)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


class PrivateAuthorApiTest(TestCase):
    """Test the authenticated user authors API"""

    def setUp(self):
        self.user = UserFactory()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_authors(self):
        """Test retrieving authors"""
        AuthorFactory.create_batch(2)

        res = self.client.get(AUTHORS_URL)

        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_author_successful(self):
        """Test creating a new author"""
        payload = {'name': 'New Author', 'bio': 'Author Bio'}
        res = self.client.post(AUTHORS_URL, payload)

        exists = Author.objects.filter(name=payload['name']).exists()
        self.assertTrue(exists)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_author_invalid(self):
        """Test creating a new author with invalid data"""
        payload = {'name': ''}
        res = self.client.post(AUTHORS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
