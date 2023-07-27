from django.urls import path, include

from .views import FeedView, PostDetailsView, PostDeleteView, CommentDeleteView, like_post, unlike_post

urlpatterns = [
    path('', FeedView.as_view(), name='feed_page'),
    path('post/<int:pk>/', include([
        path('', PostDetailsView.as_view(), name="post_details"),
        path('like/', like_post, name="like_post"),
        path('unlike/', unlike_post, name="unlike_post"),
        path('delete/', PostDeleteView.as_view(), name="post_delete"),
        path('comment/<int:comment_pk>/delete/', CommentDeleteView.as_view(), name="comment_delete")
        ])
    ),

]
