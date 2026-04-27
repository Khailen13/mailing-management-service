from django import template

register = template.Library()


@register.filter()
def media_filter(path):
    if path:
        return f"/media/{path}"
    return "#"


@register.filter
def get_value_from_dict(dict_data, key):
    return dict_data.get(key)
