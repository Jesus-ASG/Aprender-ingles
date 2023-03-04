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