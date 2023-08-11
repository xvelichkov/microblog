from django.db import models
from django.contrib.auth import get_user_model
from apps.hashtags.models import Hashtag

UserModel = get_user_model()


class Post(models.Model):
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    body = models.TextField(max_length=320)
    timestamp = models.DateTimeField(auto_now=True)
    image = models.URLField(blank=True, null=True)
    hashtags = models.ManyToManyField(Hashtag, blank=True)

    class Meta:
        ordering = ['-timestamp']

    @property
    def short_body(self):
        if len(self.body) < 30:
            return self.body

        return f'{self.body[:30]}...'

    def __str__(self):
        return self.short_body


class Comment(models.Model):
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    body = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-timestamp']

    @property
    def short_body(self):
        if len(self.body) < 30:
            return self.body

        return f'{self.body[:30]}...'

    def __str__(self):
        return self.short_body


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'post'], name='unique_like'),
        ]
