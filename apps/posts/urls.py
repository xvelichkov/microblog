from django.urls import path, include

from .views import FeedView, PostDetailsView, PostDeleteView, CommentDeleteView, like_toggle

urlpatterns = [
    path('', FeedView.as_view(), name='feed_page'),
    path('post/<int:pk>/', include([
        path('', PostDetailsView.as_view(), name='post_details'),
        path('like_toggle', like_toggle, name='like_toggle'),
        path('delete/', PostDeleteView.as_view(), name='post_delete'),
    ])
    ),
    path('comment/<int:pk>/delete/',
         CommentDeleteView.as_view(), name='comment_delete')
]
