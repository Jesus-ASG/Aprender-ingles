from django.db import models
from django.utils.text import slugify

prefix = ''


class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField('username', max_length=50)
    password = models.CharField('password', max_length=150)

    def __str__(self) -> str:
        return f'id: {self.id}\nusername: {self.username}\npassword: {self.password}'


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
    cover = models.ImageField(upload_to='imagenes/portadas/', default="imagenes/portadas/book-default.png",
                              verbose_name='cover')
    description1 = models.CharField(max_length=100, null=True, blank=True, default='')
    description2 = models.CharField(max_length=100, null=True, blank=True, default='')
    route = models.SlugField(max_length=255, unique=True, null=False, default='')

    tag = models.ManyToManyField(Tag, blank=True)

    def get_portada(self):
        return self.cover.name

    def del_portada(self, to_delete):
        if to_delete != 'imagenes/portadas/book-default.png':
            self.cover.storage.delete(to_delete)

    # Override methods
    def save(self, *args, **kwargs):
        self.route = slugify(self.title1)
        super(Story, self).save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        if self.cover.name != 'imagenes/portadas/book-default.png':
            self.cover.storage.delete(self.cover.name)
        super().delete()

    def __str__(self):
        return f'id: {self.id} | titulo: {self.title1[:5]}...'
# -------- -------- -------- --------


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
    image = models.ImageField(upload_to='imagenes/img-pages/')
    element_number = models.IntegerField()


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


# Pregunta y respuestas de opción múltiple
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
