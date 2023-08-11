
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views import generic as views
from django.contrib.auth import get_user_model

from .forms import SignupForm, ProfileEditForm
from apps.followers.models import Follower
from apps.posts.forms import PostModelForm
from apps.posts.models import Like

from utils.mixins import PaginatorMixin, AuthorizationRequiredMixin

UserModel = get_user_model()


class AccountLoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

class AccountLogoutView(LoginRequiredMixin, auth_views.LogoutView):
    pass

class SignupView(views.CreateView):
    form_class = SignupForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('login_page')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('profile_page', pk=request.user.pk)

        return super().dispatch(request, *args, **kwargs)


class ProfileViewMixin(views.DetailView):
    model = UserModel

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context["is_following"] = Follower.objects.filter(user=self.object, follower=self.request.user).exists()
        return context

class ProfilePostsView(LoginRequiredMixin, PaginatorMixin, views.edit.FormMixin, ProfileViewMixin):
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

class ProfileFollowersView(LoginRequiredMixin, PaginatorMixin, ProfileViewMixin):
    template_name = 'accounts/profile_followers.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  
        followers = self.get_paginated_content(self.object.followers.all())
        context["object_list"] = followers
        context["page_obj"] = followers
        return context
    
class ProfileFollowingView(LoginRequiredMixin, PaginatorMixin, ProfileViewMixin):
    template_name = 'accounts/profile_following.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  
        following = self.get_paginated_content(self.object.following.all())
        context["object_list"] = following
        context["page_obj"] = following
        return context
    
class ProfileEditView(LoginRequiredMixin, AuthorizationRequiredMixin, views.edit.UpdateView):
    template_name = 'accounts/edit.html'
    form_class = ProfileEditForm
    model = UserModel
    
    def get_success_url(self):
        return reverse_lazy('profile_page', kwargs={"pk":self.object.pk})


class ProfileDeleteView(LoginRequiredMixin, AuthorizationRequiredMixin, views.edit.DeleteView):
    template_name = 'accounts/delete.html'
    model = UserModel

    success_url = reverse_lazy("login_page")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_to_delete = UserModel.objects.get(pk=self.kwargs.get("pk"))
        context["username"] = "your" if user_to_delete == self.request.user else f"@{user_to_delete.username}"
        return context
    