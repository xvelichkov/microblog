from django.shortcuts import redirect, get_object_or_404

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from .models import Follower

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