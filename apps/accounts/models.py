from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy


class AccountUser(AbstractUser):
    first_name = models.CharField("first name", max_length=150)
    last_name = models.CharField("last name", max_length=150)
    email = models.EmailField("email address", unique=True)


    def unread_notifications(self):
        return self.notifications.filter(is_read=False)

    def unread_notificaitons_count(self):
        return self.unread_notifications().count()

UserModel = get_user_model()


