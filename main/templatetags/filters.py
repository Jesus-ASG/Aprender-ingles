from django import template

register = template.Library()

@register.filter
def filter_stories(stories, search_string):
    if search_string:
        stories = stories.filter(title1__icontains=search_string)
    return stories


@register.filter
def to_str(x):
    return f'{x}'


@register.filter
def to_int(x):
    return int(x)


@register.filter
def decimal_part(x, decimals=2):
    x = x - int(x)
    return round(x, decimals)


@register.filter
def cut_str(x, n):
    if len(x) > n:
        return x[:n].strip() + '...'
    else:
        return x
    
@register.filter
def page_type_to_str(x):
    match x:
        case 1:
            return "Plantilla general"
        case 2:
            return "Video y ejercicios"
        case 3:
            return "Diseño libre"