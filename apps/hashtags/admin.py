from django.contrib import admin
from django.db.models import Count
from .models import Hashtag


@admin.register(Hashtag)
class HashtagAdmin(admin.ModelAdmin):
    list_display = ('name', 'posts')
    search_fields = ('name', )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(posts_count=Count('post'))
        return qs

    def posts(self, obj):
        return obj.posts_count
    posts.admin_order_field = 'posts_count'
