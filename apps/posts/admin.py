from typing import Any
from django.contrib import admin
from django.db.models import Count
from .models import Post, Comment, Like

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'short_body', 'timestamp', 'likes', 'comments')
    search_fields = ('author__username', 'body')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(likes_count=Count('like'))
        qs = qs.annotate(comments_count=Count('comment'))
        return qs

    def likes(self, obj):
        return obj.likes_count
    likes.admin_order_field = 'likes_count'

    def comments(self, obj):
        return obj.comments_count
    comments.admin_order_field = 'comments_count'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'short_body', 'timestamp', 'post')
    search_fields = ('user__username', 'body')


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post')
    search_fields = ('user__username', 'post__body')
