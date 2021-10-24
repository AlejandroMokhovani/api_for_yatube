from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from django.db.models import Q, F

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True)
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE,
        related_name="posts", blank=True, null=True
    )

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    def __str__(self):
        return self.text


class Follow(models.Model):
    # Ссылка на объект пользователя, который подписывается
    user = models.ForeignKey(
        User, related_name="follower", on_delete=models.CASCADE,
    )
    # Ссылка на объект пользователя, на которого подписываются
    following = models.ForeignKey(
        User, related_name="following", blank=True, null=True,
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='unique_following'
            ),

            models.CheckConstraint(
                check=~Q(user=F("following")),
                name='dont follow youself'
            ),
        ]
