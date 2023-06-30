import uuid
import random
from django.conf import settings

from django.db import models
from django.utils.text import slugify
from PIL import Image as pil_image
from io import BytesIO
from django.core.files import File
from django.core.files.base import ContentFile

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

from django.contrib.auth.models import User


prefix = ''
default_cover_img_path = 'main/static/img/default-cover.png'


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


# Tag
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
    title1 = models.CharField(max_length=255)
    title2 = models.CharField(max_length=255)
    cover = models.ImageField(upload_to=settings.IMAGES_PATH, default=default_cover_img_path, verbose_name='cover')
    description1 = models.CharField(max_length=255, null=False, blank=True, default='')
    description2 = models.CharField(max_length=255, null=False, blank=True, default='')
    
    xp_required = models.IntegerField(default=0)

    tags = models.ManyToManyField(Tag, blank=True)

    likes_number = models.IntegerField(default=0)
    route = models.SlugField(max_length=255, unique=True, null=False, default='')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def get_portada(self):
        return self.cover.name

    def del_portada(self, to_delete):
        if to_delete != default_cover_img_path:
            self.cover.storage.delete(to_delete)

    # Override methods
    def save(self, *args, **kwargs):
        if not self.likes_number:
            self.likes_number = random.randint(270, 300)
        self.route = slugify(self.title1)

        if self.cover.name != default_cover_img_path:
            resizeImage(self.cover, (800, 800))
        super(Story, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.cover.name != default_cover_img_path:
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
    # key for link one to one to the django user
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # extra fields
    scored_stories = models.ManyToManyField(Story, related_name='users_scored', through='Score')
    liked_stories = models.ManyToManyField(Story, related_name='users_liked', through='LikedStory')
    saved_stories = models.ManyToManyField(Story, related_name='saved_by', through='SavedStory')

    xp = models.IntegerField(default=0)
    level = models.FloatField(default=1)

    DEFAULT_PROFILE_IMAGE_CHOICES = [
        ('/static/img/profile_pictures/pp1.jpg', 'Friendly bear'),
        ('/static/img/profile_pictures/pp2.jpg', 'Thoughtful cat'),
        ('/static/img/profile_pictures/pp3.jpg', 'Hungry panda'),
        ('/static/img/profile_pictures/pp4.jpg', 'Cute Hamster'),
        ('/static/img/profile_pictures/pp5.jpg', 'Tall giraffe'),
        ('/static/img/profile_pictures/pp6.jpg', 'Chilly bird'),
    ]
    default_profile_image = models.CharField(max_length=50, choices=DEFAULT_PROFILE_IMAGE_CHOICES, blank=True, null=True)

    def __str__(self) -> str:
        return f'username: {self.user.username}'


class LikedStory(models.Model):
    class Meta:
        db_table = prefix + 'liked_story'
    # keys
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)

    # fields
    date = models.DateTimeField(auto_now_add=True, null=True)


class SavedStory(models.Model):
    class Meta:
        db_table = prefix + 'saved_story'
    # keys
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)

    # fields
    date = models.DateTimeField(auto_now_add=True, null=True)


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
    score_percentage = models.FloatField(default=0)
    writing_percentage = models.FloatField(default=100)
    comprehension_percentage = models.FloatField(default=100)
    speaking_percentage = models.FloatField(default=100)
    
    def __str__(self) -> str:
        string = f"""
            date: {self.date}
            username: {self.user_profile.user.username}
            story: {self.story.title1}
            score_percentage: {self.score_percentage}
            """
        #f'username: {self.user_profile.user.username}, story: {self.story.title1}, score: {self.score}'
        return string


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

"""
# Audio
class Audio(models.Model):
    class Meta:
        db_table = prefix + 'audio'
    
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='audios')
    # fields
    element_number = models.IntegerField()
    url = models.FileField(upload_to=settings.AUDIOS_PATH+'%Y/%m/%d/', null=True, blank=True)

    def getFormat(self):
        extension = self.url.split('.')[-1]
        match extension:
            case 'mp3':
                return 'audio/mpeg'
            case 'ogg':
                return 'audio/ogg'
            case 'wav':
                return 'audio/wav'
"""

# Video
class Video(models.Model):
    class Meta:
        db_table = prefix + 'video'
    # keys
    id = models.AutoField(primary_key=True)
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='videos')
    # fields
    element_number = models.IntegerField()
    url = models.CharField(max_length=2048)


# Image
class Image(models.Model):
    class Meta:
        db_table = prefix + 'image'
    # keys
    id = models.AutoField(primary_key=True)
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='images')
    # fields
    element_number = models.IntegerField()
    image = models.ImageField(upload_to=settings.IMAGES_PATH, null=True, blank=True)
    

    # Override methods
    def delete(self, *args, **kwargs):
        self.image.delete(save=False)
        super(Image, self).delete(*args, **kwargs)



# Text
class Text(models.Model):
    class Meta:
        db_table = prefix + 'text'
    # keys
    id = models.AutoField(primary_key=True)
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='texts')
    
    language1 = models.TextField(null=False, blank=False)
    language2 = models.TextField(null=False, blank=False)
    element_number = models.IntegerField()

    def __str__(self) -> str:
        return f'id: {self.id}, l1: {self.language1}, l2: {self.language2}'


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
    show_text = models.BooleanField(default=True)
    element_number = models.IntegerField()

    def __str__(self) -> str:
        return f'{self.page.id} - {self.content1}'


# Spellcheck
class Spellcheck(models.Model):
    class Meta:
        db_table = prefix + 'spellcheck'

    # keys
    id = models.AutoField(primary_key=True)
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='spellchecks')
    # fields
    element_number = models.IntegerField()
    wrong_text = models.CharField(max_length=600)
    right_text = models.CharField(max_length=600)
    translated_right_text = models.CharField(max_length=600)


# Question
class MultipleChoiceQuestion(models.Model):
    class Meta:
        db_table = prefix + 'multiple_choice_question'
    # keys
    id = models.AutoField(primary_key=True)
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='questions')
    # fields
    element_number = models.IntegerField()
    text = models.CharField(max_length=255)
    t_text = models.CharField(max_length=255)
    randomize_choices = models.BooleanField(default=True)
    

# Question Option
class QuestionChoice(models.Model):
    class Meta:
        db_table = prefix + 'question_choice'
    # keys
    id = models.AutoField(primary_key=True)
    question = models.ForeignKey(MultipleChoiceQuestion, on_delete=models.CASCADE, related_name='choices')
    # fields
    choice_number = models.IntegerField(default=0)
    text = models.CharField(max_length=255)
    t_text = models.CharField(max_length=255)
    correct = models.BooleanField(default=False)


class UserAnswer(models.Model):
    class Meta:
        db_table = prefix + 'user_answer'

    # keys
    id = models.AutoField(primary_key=True)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='answers')
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    # Key for different exercises
    exercise_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    exercise_id = models.PositiveIntegerField()
    exercise = GenericForeignKey('exercise_type', 'exercise_id')
    # fields
    answer = models.CharField(max_length=255, blank=True, default='')
    submited = models.BooleanField(default=False)
    evaluated = models.BooleanField(default=False)

    def __str__(self) -> str:
        string = f'{self.user_profile.id} - {self.story.id} - {self.page.id}\n'
        string += f'{self.exercise_type}, {self.exercise_id}, {self.exercise}\n'
        string += f'{self.answer} -- {self.submited}'
        return string


class FlashcardCollection(models.Model):
    class Meta:
        db_table = prefix + 'flashcard_collection'

    # keys
    id = models.AutoField(primary_key=True)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='flashcards_collections')

    # fields
    color = models.CharField(max_length=7, default='#cbe5ff')
    collection_name = models.CharField(max_length=100, blank=False, null=False, default='New Collection')
    description = models.CharField(max_length=255, blank=True, default='')
    
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


class Flashcard(models.Model):
    class Meta:
        db_table = prefix + 'flashcard'

    # keys
    id = models.AutoField(primary_key=True)
    flashcard_collection = models.ForeignKey(FlashcardCollection, on_delete=models.CASCADE, related_name='flashcards')

    # fields
    color = models.CharField(max_length=7, default='#cbe5ff')
    front = models.CharField(max_length=255)
    back = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


class CBRSettings(models.Model):
    class Meta:
        db_table = prefix + 'cbr_settings'

    # keys
    id = models.AutoField(primary_key=True)
    # fields
    timeout = models.IntegerField(default=0)
    update_on_alter_stories = models.BooleanField(default=True)

    def __str__(self) -> str:
        return 'Timeout: {}, Update: {}'.format(self.timeout, self.update_on_alter_stories)


class UBRSettings(models.Model):
    class Meta:
        db_table = prefix + 'ubr_settings'

    # keys
    id = models.AutoField(primary_key=True)
    # fields
    timeout = models.IntegerField(default=1800)

    def __str__(self) -> str:
        return 'Timeout: {}'.format(self.timeout)

