from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied


class PaginatorMixin:
    paginated_by = 10
    page_kwarg = "page"

    def get_paginated_content(self, queryset):
        paginator = Paginator(queryset, self.paginated_by)
        page = self.kwargs.get(self.page_kwarg) or self.request.GET.get(self.page_kwarg) or 1
        return paginator.get_page(page)
    
class AuthorizationRequiredMixin:
    authorization_attribute_name = None
    staff_allowed = True

    def check_authorized(self, user, obj):
        obj_to_check = obj
        if self.authorization_attribute_name and hasattr(obj, self.authorization_attribute_name):
            obj_to_check = getattr(obj, self.authorization_attribute_name)

        if (self.staff_allowed and not user.is_staff) and (user != obj_to_check):
            raise PermissionDenied("You are not allowed to perform this action.")

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        self.check_authorized(request.user, obj)

        return super().dispatch(request, *args, **kwargs)