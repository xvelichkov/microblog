from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post
from apps.hashtags.models import Hashtag

from utils.helpers import get_hashtags


@receiver(post_save, sender=Post)
def add_hashtag_to_post(sender, instance, created, **kwargs):
    if created:
        hashtags = get_hashtags(instance.body)

        for hashtag in hashtags:
            hashtag, _ = Hashtag.objects.get_or_create(name=hashtag)
            instance.hashtags.add(hashtag)
