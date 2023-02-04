from django.contrib import admin
from .models import Tag, Story, Page, Image, Dialogue, RepeatPhrase, Score, UserProfile, SavedStory

admin.site.register(Tag)
admin.site.register(Story)
admin.site.register(Page)
admin.site.register(Image)
admin.site.register(Dialogue)
admin.site.register(RepeatPhrase)
admin.site.register(Score)
admin.site.register(UserProfile)
admin.site.register(SavedStory)