from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy

from django.views import generic as views

from .models import Notification

@login_required
def read_notification(request, pk):
    notification = get_object_or_404(Notification, id=pk)

    if notification.target_user != request.user:
        raise PermissionDenied("You are not allowed to perform this action.")

    notification.is_read = True
    notification.save()

    next = request.GET.get('next', reverse_lazy('notifications_page'))

    return redirect(next)


class NotificationListView(LoginRequiredMixin, views.ListView):
    template_name = 'notifications/list.html'
    model = Notification
    paginate_by = 30

    def get_queryset(self):
        return self.request.user.notifications.all()