from django.core.paginator import Paginator


class PaginatorMixin:
    paginated_by = 10
    page_kwarg = "page"

    def get_paginated_content(self, queryset):
        paginator = Paginator(queryset, self.paginated_by)
        page = self.kwargs.get(self.page_kwarg) or self.request.GET.get(self.page_kwarg) or 1
        return paginator.get_page(page)