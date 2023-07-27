from django import template
from django.urls import reverse_lazy

from utils.helpers import MENTION_REGEX, HASHTAG_REGEX
from django.contrib.auth import get_user_model
from apps.hashtags.models import Hashtag

import re

UserModel = get_user_model()
register = template.Library()

@register.filter
def decorate_mentions(value):
    def wrap(match):
        try:
            username = match.group(1)
            user = UserModel.objects.get(username=username)
            profile_page = reverse_lazy('profile_page', kwargs={"pk":user.pk})
            return f'<a class="text-decoration-none" href={profile_page}>{match.group()}</a>'
        except UserModel.DoesNotExist:
            pass

        return match.group()
    
    return re.sub(MENTION_REGEX, wrap, value)

@register.filter
def decorate_hashtags(value):
    def wrap(match):
        try:
            hashtag = Hashtag.objects.get(name=match.group(1))
            profile_page = reverse_lazy('hashtag_page', kwargs={"pk":hashtag.pk})
            return f'<a class="text-decoration-none" href={profile_page}>{match.group()}</a>'
        except Hashtag.DoesNotExist:
            pass

        return match.group()
    
    return re.sub(HASHTAG_REGEX, wrap, value)