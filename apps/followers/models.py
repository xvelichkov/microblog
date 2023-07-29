from django.db import models
from django.contrib.auth import get_user_model

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

