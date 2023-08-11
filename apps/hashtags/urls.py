from django.urls import path
from .views import HashtagView

urlpatterns = [
    path('<int:pk>/', HashtagView.as_view(), name='hashtag_page')
]
