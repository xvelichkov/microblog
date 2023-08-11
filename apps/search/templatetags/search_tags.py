from django import template
from apps.search.forms import SearchForm

register = template.Library()


@register.simple_tag
def search_form():
    return SearchForm()
