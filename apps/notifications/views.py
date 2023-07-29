from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views import generic as views

from .models import Notification

@login_required
def read_notification(request, pk):
    notification = get_object_or_404(Notification, id=pk)

    notification.is_read = True
    notification.save()

    next = request.GET.get('next')

    return redirect(next)


class NotificationListView(LoginRequiredMixin, views.ListView):
    template_name = 'notifications/list.html'
    model = Notification
    paginate_by = 10