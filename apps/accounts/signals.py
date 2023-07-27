from django.db.models.signals import post_save
from django.contrib.auth import get_user_model

from django.dispatch import receiver

from .models import Notification, Follower
from utils.helpers import get_mentions


UserModel = get_user_model()

@receiver(post_save, sender='posts.Like')
def create_like_notification(sender, instance, created, **kwargs):
    if created and instance.user != instance.post.author:
        Notification.objects.create(
            user = instance.user,
            target_user = instance.post.author,
            type = Notification.NotificationTypes.LIKE,
            post = instance.post
        )

@receiver(post_save, sender=Follower)
def create_follow_notification(sender, instance, created, **kwargs):
    if created and instance.follower != instance.user:
        Notification.objects.create(
            user = instance.follower,
            target_user = instance.user,
            type = Notification.NotificationTypes.FOLLOW
        )

def create_mention_notification(instance, is_post=True):
    if instance:
        for mention in get_mentions(instance.body):
                try:
                    target_user = UserModel.objects.get(username=mention)
                    if instance.author != target_user:
                        notification = Notification(
                            user = instance.author,
                            target_user = target_user,
                            type = Notification.NotificationTypes.MENTION,
                        )

                        if is_post:
                            notification.post = instance
                        else:
                            notification.post = instance.post
                            notification.comment = instance

                        notification.save()

                except UserModel.DoesNotExist:
                    pass


@receiver(post_save, sender='posts.Comment')
def create_comment_notification(sender, instance, created, **kwargs):
    if created:
        if instance.author != instance.post.author:
            Notification.objects.create(
                user = instance.author,
                target_user = instance.post.author,
                type = Notification.NotificationTypes.COMMENT,
                comment = instance,
                post = instance.post
            )

        create_mention_notification(instance, is_post=False)
       

