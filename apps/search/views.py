from django.views import generic as views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model

from apps.posts.models import Post
from apps.hashtags.models import Hashtag

UserModel = get_user_model()


class SearchPostsView(LoginRequiredMixin, views.ListView):
    template_name = 'search/result_posts.html'
    paginate_by = 10

    def get_queryset(self):
        q = self.request.GET.get("q", "")
        if q:
            posts = Post.objects.filter(body__icontains=q) | Post.objects.filter(author__username__icontains=q) | Post.objects.filter(
                author__first_name__icontains=q) | Post.objects.filter(author__last_name__icontains=q)

            return posts
        return []


class SearchUsersView(LoginRequiredMixin, views.ListView):
    template_name = 'search/result_users.html'
    paginate_by = 10

    def get_queryset(self):
        q = self.request.GET.get("q", "")
        if q:
            users = UserModel.objects.filter(username__icontains=q) | UserModel.objects.filter(
                first_name__icontains=q) | UserModel.objects.filter(last_name__icontains=q)

            return users
        return []


class SearchHashtagView(LoginRequiredMixin, views.ListView):
    template_name = 'search/result_hashtags.html'
    paginate_by = 10

    def get_queryset(self):
        q = self.request.GET.get("q", "")

        if q:
            hashtags = Hashtag.objects.filter(name__icontains=q)

            return hashtags
        return []
