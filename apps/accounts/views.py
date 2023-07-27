from typing import Any, Dict
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import get_user_model

from .forms import SignupForm, ProfileEditForm
from apps.posts.forms import PostModelForm
from apps.posts.models import Like
from .models import Follower, Notification
from django.core.paginator import Paginator

from utils.mixins import PaginatorMixin

UserModel = get_user_model()

@login_required
def follow_user(request, pk):

    user_to_follow = get_object_or_404(UserModel, id=pk)

    # Ensure the user is not trying to follow themselves
    if request.user != user_to_follow:
        Follower.objects.get_or_create(user=user_to_follow, follower=request.user)
    
    return redirect('profile_page', pk=pk)

@login_required
def unfollow_user(request, pk):
    user_to_unfollow = get_object_or_404(UserModel, id=pk)
    
    follower_filter = Follower.objects.filter(user=user_to_unfollow, follower=request.user)

    # Ensure the user is not trying to unfollow themselves
    if request.user != user_to_unfollow and follower_filter.exists():
        follower_filter.delete()
    
    return redirect('profile_page', pk=pk)

@login_required
def read_notification(request, pk):
    notification = get_object_or_404(Notification, id=pk)

    notification.is_read = True
    notification.save()

    next = request.GET.get('next')

    return redirect(next)


class NotificationListView(views.ListView):
    template_name = 'notifications/list.html'
    model = Notification
    paginate_by = 10

class AccountLoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

class AccountLogoutView(auth_views.LogoutView):
    pass

class SignupView(views.CreateView):
    form_class = SignupForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('login_page')


class ProfileViewMixin(LoginRequiredMixin, views.DetailView):
    model = UserModel

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context["is_following"] = Follower.objects.filter(user=self.object, follower=self.request.user).exists()
        return context

class ProfilePostsView(views.edit.FormMixin, PaginatorMixin, ProfileViewMixin):
    form_class = PostModelForm
    template_name = 'accounts/profile_posts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  
        posts = self.get_paginated_content(self.object.post_set.all())
        for post in posts:
            post.liked = Like.objects.filter(user=self.request.user, post=post).exists()
        
        context["object_list"] = posts
        context["page_obj"] = posts

        return context
    
    def get_success_url(self):
        return reverse_lazy('profile_page', kwargs={"pk":self.request.user.pk})

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

class ProfileFollowersView(PaginatorMixin, ProfileViewMixin):
    template_name = 'accounts/profile_followers.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  
        followers = self.get_paginated_content(self.object.followers.all())
        context["object_list"] = followers
        context["page_obj"] = followers
        return context
    
class ProfileFollowingView(PaginatorMixin, ProfileViewMixin):
    template_name = 'accounts/profile_following.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  
        following = self.get_paginated_content(self.object.following.all())
        context["object_list"] = following
        context["page_obj"] = following
        return context
    
class ProfileEditView(LoginRequiredMixin, views.edit.UpdateView):
    template_name = 'accounts/edit.html'
    form_class = ProfileEditForm
    model = UserModel
    
    def get_success_url(self):
        return reverse_lazy('profile_page', kwargs={"pk":self.object.pk})


class ProfileDeleteView(LoginRequiredMixin, views.edit.DeleteView):
    template_name = 'accounts/delete.html'
    model = UserModel

    success_url = reverse_lazy("login_page")