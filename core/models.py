from django.db import models
from django_ckeditor_5.fields import CKEditor5Field


class Topic(models.Model):
    name = models.CharField(verbose_name="Title", max_length=200)


class Post(models.Model):
    title = models.CharField(verbose_name="Title", max_length=200)
    topic = models.ForeignKey(verbose_name="Topic", to=Topic, on_delete=models.CASCADE)
    content = CKEditor5Field(verbose_name="Content")
    author = models.ForeignKey(verbose_name="Author", to="Author", on_delete=models.CASCADE)
    pub_date = models.DateTimeField(verbose_name="Publish Date", auto_now_add=True)

    def __str__(self):
        return self.title


class Author(models.Model):
    name = models.CharField(verbose_name="Name", max_length=150)
    bio = models.TextField(verbose_name="auther bio")

    def __str__(self):
        return self.name


__all__ = [
    "Author",
    "Post",
    "Topic"
]
