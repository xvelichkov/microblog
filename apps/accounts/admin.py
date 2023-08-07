from typing import Any
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.db.models import Count

UserModel = get_user_model()

@admin.register(UserModel)
class AccountUserAdmin(UserAdmin):
    pass
