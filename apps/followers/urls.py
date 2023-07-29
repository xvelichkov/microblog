from django.urls import path, include
from .views import follow_user, unfollow_user

urlpatterns = [
    path('<int:pk>/', include([
        path('follow/', follow_user, name='follow_user'),
        path('unfollow/', unfollow_user, name='unfollow_user')
    ])),
]
