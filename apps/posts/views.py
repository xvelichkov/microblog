from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from django.views import generic as views
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from .models import Post, Like, Comment
from .forms import CommentModelForm, PostModelForm
from utils.mixins import PaginatorMixin, AuthorizationRequiredMixin


@login_required
def like_toggle(request, pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=pk)
        user = request.user

        if Like.objects.filter(user=user, post=post).exists():
            Like.objects.filter(user=user, post=post).delete()
        else:
            Like.objects.create(user=user, post=post)

        return JsonResponse({
            'like_count': post.like_set.count()
        })

    # as GET method is not supported redirect to post details page
    return redirect('post_details', pk=pk)


class FeedView(LoginRequiredMixin,  views.edit.FormMixin, views.ListView):
    template_name = 'posts/feed.html'
    model = Post
    form_class = PostModelForm
    success_url = reverse_lazy('feed_page')
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return super().form_valid(form)

    def get_queryset(self):
        objects = Post.objects.filter(
            author__followers__follower=self.request.user) | Post.objects.filter(author=self.request.user)
        objects = objects.distinct()
        for object in objects:
            object.liked = Like.objects.filter(
                user=self.request.user, post=object).exists()

        return objects


class PostDetailsView(LoginRequiredMixin, PaginatorMixin, views.edit.FormMixin, views.DetailView):
    template_name = 'posts/details.html'
    model = Post
    form_class = CommentModelForm

    def get_object(self, *args, **kwargs):
        obj = super().get_object(*args, **kwargs)
        obj.liked = Like.objects.filter(
            user=self.request.user, post=obj).exists()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = self.get_paginated_content(self.object.comment_set.all())
        context['page_obj'] = comments
        context['comments'] = comments
        return context

    def get_success_url(self):
        return reverse_lazy('post_details', kwargs={'pk': self.object.pk})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.post = self.object
        comment.save()
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, AuthorizationRequiredMixin, views.edit.DeleteView):
    model = Post
    template_name = 'posts/delete.html'
    success_url = reverse_lazy('feed_page')
    authorization_attribute_name = 'author'


class CommentDeleteView(LoginRequiredMixin, AuthorizationRequiredMixin, views.edit.DeleteView):
    model = Comment
    authorization_attribute_name = 'author'

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER', reverse_lazy('post_details', kwargs={'pk': self.object.post}))

    # skip confirmation page
    def get(self, *args, **kwargs):
        return self.delete(*args, **kwargs)
