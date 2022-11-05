from django.contrib import admin
from .models import User, Tag, Story, Page

admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Story)
admin.site.register(Page)
