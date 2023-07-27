from django.db import models

class Hashtag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ('name',)