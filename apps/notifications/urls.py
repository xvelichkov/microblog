  
from django.urls import path
from .views import read_notification, NotificationListView

urlpatterns = [
    path('', NotificationListView.as_view(), name="notifications_page"),
    path('<int:pk>/', read_notification, name='read_notification')
]

