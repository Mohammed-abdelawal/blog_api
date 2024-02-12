import datetime

from django.db import models
from django_ckeditor_5.fields import CKEditor5Field


class Topic(models.Model):
    """
    Model representing a topic in the blog.

    Attributes:
        name (str): The name/title of the topic.
    """
    name: str = models.CharField(verbose_name="Title", max_length=200)

    def __str__(self) -> str:
        """
        Returns a string representation of the topic.
        """
        return self.name


class Author(models.Model):
    """
    Model representing an author of the posts.

    Attributes:
        name (str): The name of the author.
        bio (str): A brief biography of the author.
    """
    name: str = models.CharField(verbose_name="Name", max_length=150)
    bio: str = models.TextField(verbose_name="Author Bio")

    def __str__(self) -> str:
        """
        Returns a string representation of the author.
        """
        return self.name


class Post(models.Model):
    """
    Model representing a blog's post.

    Attributes:
        title (str): The title of the blog post.
        topic (Topic): The topic associated with the post.
        content (str): The content/body of the blog post.
        author (Author): The author of the blog post.
        pub_date (datetime.datetime): The date and time when the post was published.
    """
    title: str = models.CharField(verbose_name="Title", max_length=200)
    topic: Topic = models.ForeignKey(
        verbose_name="Topic",
        to=Topic,
        on_delete=models.CASCADE
    )
    content: str = CKEditor5Field(verbose_name="Content")
    author: Author = models.ForeignKey(
        verbose_name="Author",
        to="Author",
        on_delete=models.CASCADE
    )
    pub_date: datetime.datetime = models.DateTimeField(
        verbose_name="Publish Date",
        auto_now_add=True
    )

    def __str__(self) -> str:
        """
        Returns a string representation of the post.
        """
        return self.title


__all__ = [
    "Author",
    "Post",
    "Topic"
]
