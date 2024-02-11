import factory.fuzzy
from django.contrib.auth import get_user_model

from core.models import Author, Topic, Post

UserModel = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserModel
        django_get_or_create = ("email", "username")

    first_name = "user"
    last_name = factory.Sequence(lambda n: str(n))
    username = factory.Sequence(lambda n: f"user{n}_{n * n}")
    email = factory.Sequence(lambda n: f"user{n}@example.com")
    password = factory.PostGenerationMethodCall("set_password", "passw0rd")
    is_staff = False
    is_superuser = False


class TopicFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Topic

    name = factory.Faker('sentence', nb_words=3)


class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Author

    name = factory.Faker('name')
    bio = factory.Faker('text')


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    title = factory.Faker('sentence', nb_words=4)
    topic = factory.SubFactory(TopicFactory)
    content = factory.Faker('paragraph')
    author = factory.SubFactory(AuthorFactory)
    pub_date = factory.Faker('date_time_this_year')
