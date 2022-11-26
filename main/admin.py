from django.contrib import admin
from .models import User, Tag, Story, Page, Image, Dialogue

admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Story)
admin.site.register(Page)
admin.site.register(Image)
admin.site.register(Dialogue)
