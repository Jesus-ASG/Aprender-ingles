import uuid
import random

from django.db import models
from django.utils.text import slugify
from PIL import Image as pil_image
from io import BytesIO
from django.core.files import File
from django.core.files.base import ContentFile

from django.contrib.auth.models import User


def resizeImage(imageField, tupleSize):
    im = pil_image.open(imageField)  # Catch original
    source_image = im
    #source_image = im.convert('RGB') # Uncomment for put solid background
    source_image.thumbnail(tupleSize)  # Resize to size
    output = BytesIO()
    source_image.save(output, format='PNG') # Save resize image to bytes
    output.seek(0)

    content_file = ContentFile(output.read())  # Read output and create ContentFile in memory
    file = File(content_file)

    random_name = f'{uuid.uuid4()}.png'
    imageField.save(random_name, file, save=False)


prefix = ''


# Categoría
class Tag(models.Model):
    class Meta:
        db_table = prefix + 'tag'

    # keys
    id = models.AutoField(primary_key=True)
    # fields
    name1 = models.CharField(max_length=100)
    name2 = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name1
# -------- -------- -------- --------


# Story
class Story(models.Model):
    class Meta:
        db_table = prefix + 'story'

    # primary key
    id = models.AutoField(primary_key=True)
    # fields
    title1 = models.CharField(max_length=100)
    title2 = models.CharField(max_length=100)
    cover = models.ImageField(upload_to='imagenes/portadas/', 
                              default="imagenes/portadas/book-default.png",
                              verbose_name='cover')
    description1 = models.CharField(max_length=100, null=True, blank=True, default='')
    description2 = models.CharField(max_length=100, null=True, blank=True, default='')
    route = models.SlugField(max_length=255, unique=True, null=False, default='')

    tag = models.ManyToManyField(Tag, blank=True)

    likes_number = models.IntegerField(default=0)

    def get_portada(self):
        return self.cover.name

    def del_portada(self, to_delete):
        if to_delete != 'imagenes/portadas/book-default.png':
            self.cover.storage.delete(to_delete)

    # Override methods
    def save(self, *args, **kwargs):
        if not self.likes_number:
            self.likes_number = random.randint(270, 300)
        self.route = slugify(self.title1)
        if self.cover.name != 'imagenes/portadas/book-default.png':
            resizeImage(self.cover, (800, 800))
        super(Story, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.cover.name != 'imagenes/portadas/book-default.png':
            self.cover.storage.delete(self.cover.name)
        
        # delete pages related
        for page in self.pages.all():
            page.delete()
        # delete story
        super(Story, self).delete(*args, **kwargs)

    def __str__(self):
        return f'title: {self.title1}'
# -------- -------- -------- --------


class UserProfile(models.Model):
    class Meta:
        db_table = prefix + 'user_profile'
    # link one to one to the django user
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # extra fields
    stories_scores = models.ManyToManyField(Story, through='Score', related_name='users_scored')
    liked_stories = models.ManyToManyField(Story, related_name='users_liked', blank=True)

    def __str__(self) -> str:
        return f'username: {self.user.username}'


class Score(models.Model):
    class Meta:
        db_table = prefix + 'score'
    # keys
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    # fields
    date = models.DateTimeField(auto_now_add=True, null=True)

    # Score punctuation
    score = models.IntegerField(default=0)
    score_limit = models.IntegerField(default=1)

    # Percentages
    writing_percentage = models.FloatField(default=100)
    comprehension_percentage = models.FloatField(default=100)
    speaking_percentage = models.FloatField(default=100)
    
    def __str__(self) -> str:
        return f'username: {self.user_profile.user.username}, story: {self.story.title1}, score: {self.score}'


# Page
class Page(models.Model):
    class Meta:
        db_table = prefix + 'page'
    # keys
    id = models.AutoField(primary_key=True)
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='pages')
    # fields
    subtitle1 = models.CharField(max_length=100, default="")
    subtitle2 = models.CharField(max_length=100, default="")
    page_type = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    time_created = models.TimeField(auto_now_add=True, null=True)
    
    
    def delete(self, *args, **kwargs):
        # delete images related
        for image in self.images.all():
            image.delete()
        # delete page
        super(Page, self).delete(*args, **kwargs)
# -------- -------- -------- --------


# Video
class VideoUrl(models.Model):
    class Meta:
        db_table = prefix + 'video_url'
    # keys
    id = models.AutoField(primary_key=True)
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='video_urls')
    # fields
    url = models.CharField(max_length=2048)
    element_number = models.IntegerField()


# Image
class Image(models.Model):
    class Meta:
        db_table = prefix + 'image'
    # keys
    id = models.AutoField(primary_key=True)
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='images')
    # fields
    image = models.ImageField(upload_to='imagenes/img-pages/', null=True, blank=True)
    element_number = models.IntegerField()
    
    def delete(self, *args, **kwargs):
        self.image.delete(save=False)
        super(Image, self).delete(*args, **kwargs)


# Dialogue
class Dialogue(models.Model):
    class Meta:
        db_table = prefix + 'dialogue'
    # keys
    id = models.AutoField(primary_key=True)
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='dialogues')
    # fields
    name = models.CharField(max_length=30)
    content1 = models.CharField(max_length=255)
    content2 = models.CharField(max_length=255)
    color = models.CharField(max_length=7, default='#000000')
    element_number = models.IntegerField()
# -------- -------- -------- --------


# ---------- Exercises ---------- #
# Repeat phrase
class RepeatPhrase(models.Model):
    class Meta:
        db_table = prefix + 'repeat_phrase'
    # keys
    id = models.AutoField(primary_key=True)
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='repeat_phrases')
    # fields
    content1 = models.CharField(max_length=255)
    content2 = models.CharField(max_length=255)
    element_number = models.IntegerField()
# -------- -------- -------- --------


# Ask and answer
class Question(models.Model):
    class Meta:
        db_table = prefix + 'question'
    # keys
    id = models.AutoField(primary_key=True)
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='questions')
    # fields
    question1 = models.CharField(max_length=255)
    question2 = models.CharField(max_length=255)
    element_number = models.IntegerField()


class Option(models.Model):
    class Meta:
        db_table = prefix + 'option'
    # keys
    id = models.AutoField(primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    # fields
    answer1 = models.CharField(max_length=255)
    answer2 = models.CharField(max_length=255)
    correct = models.BooleanField(default=False)
# -------- -------- -------- --------
