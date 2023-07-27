from django.urls import path
from .views import SearchPostsView, SearchUsersView, SearchHashtagView

urlpatterns = [
    path('', SearchPostsView.as_view(), name='search_result_page'),
    path('users/', SearchUsersView.as_view(), name='search_result_users_page'),
    path('hashtags/', SearchHashtagView.as_view(), name='search_result_hashtags_page')
]
