from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy


class AccountUser(AbstractUser):
    def unread_notifications(self):
        return self.notifications.filter(is_read=False)

    def unread_notificaitons_count(self):
        return self.unread_notifications().count()
    

UserModel = get_user_model()

class Follower(models.Model):
    user = models.ForeignKey(
        UserModel, related_name='followers', on_delete=models.CASCADE)
    follower = models.ForeignKey(
        UserModel, related_name='following', on_delete=models.CASCADE)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'follower'], name='unique_pair')
        ]

class Notification(models.Model):

    class Meta:
        ordering = ('is_read', '-timestamp')

    class NotificationTypes(models.IntegerChoices):
        FOLLOW = 1
        LIKE = 2
        COMMENT = 3
        MENTION = 4

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    target_user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='notifications')
    type = models.IntegerField(choices=NotificationTypes.choices)
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE, blank=True, null=True)
    comment = models.ForeignKey('posts.Comment', on_delete=models.CASCADE, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def get_absolute_url(self):
        if self.type == Notification.NotificationTypes.FOLLOW:
            next = reverse_lazy('profile_page', kwargs={"pk" : self.user.pk})
        elif self.type == Notification.NotificationTypes.LIKE:
            next = reverse_lazy('post_details', kwargs={"pk" : self.post.pk})
        elif self.type == Notification.NotificationTypes.COMMENT:
            next = reverse_lazy('post_details', kwargs={"pk" : self.post.pk})
            next += f"#comment_{self.comment.pk}"
        elif self.type == Notification.NotificationTypes.MENTION:
            next = reverse_lazy('post_details', kwargs={"pk" : self.post.pk})
            if self.comment:
                next += f"#comment_{self.comment.pk}" 

        return f"{reverse_lazy('read_notification', kwargs={'pk': self.pk})}?next={next}"

    def get_text(self):
        result = ""
        if self.type == Notification.NotificationTypes.FOLLOW:
            result += "followed you"
        elif self.type == Notification.NotificationTypes.LIKE:
            result += "liked your post"
        elif self.type == Notification.NotificationTypes.COMMENT:
            result += "commented on your post"
        elif self.type == Notification.NotificationTypes.MENTION:
            result += f"metion you in a {'comment' if self.comment else 'post'}"
        return result




