from typing import Any
from django.db.models.query import QuerySet
from django.views import generic as views
from django.contrib.auth.mixins import LoginRequiredMixin
from utils.mixins import PaginatorMixin
from .models import Hashtag
from apps.posts.models import Like

# Create your views here.
class HashtagView(LoginRequiredMixin, PaginatorMixin, views.DetailView):
    template_name = 'hashtags/hashtag.html'
    model = Hashtag

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  
        posts = self.get_paginated_content(self.object.post_set.all())
        for post in posts:
            post.liked = Like.objects.filter(user=self.request.user, post=post).exists()
        
        context["object_list"] = posts
        context["page_obj"] = posts

        return context


