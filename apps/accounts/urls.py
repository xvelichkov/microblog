from django.urls import path, include
from .views import AccountLoginView, AccountLogoutView, SignupView, ProfilePostsView, ProfileFollowersView, ProfileFollowingView, ProfileEditView, ProfileDeleteView

urlpatterns = [
    path('login/', AccountLoginView.as_view(), name='login_page'),
    path('logout/', AccountLogoutView.as_view(), name='logout_page'),
    path('signup/', SignupView.as_view(), name='signup_page'),
    path('<int:pk>/', include([
        path('', ProfilePostsView.as_view(), name='profile_page'),
        path('followers/', ProfileFollowersView.as_view(),
             name='profile_followers_page'),
        path('following/', ProfileFollowingView.as_view(),
             name='profile_following_page'),
        path('edit/', ProfileEditView.as_view(), name='profile_edit_page'),
        path('delete/', ProfileDeleteView.as_view(), name='profile_delete_page')
    ])),


]
