from django.db import models
from django.utils.text import slugify

prefix = 'main_'

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
    name = models.CharField(max_length=100, verbose_name='name')

    def __str__(self) -> str:
        return self.name
# -------- -------- -------- --------


# Historia
class Story(models.Model):
    class Meta:
        db_table = prefix + 'story'

    # primary key
    id = models.AutoField(primary_key=True)
    # fields
    title = models.CharField(max_length=100, verbose_name='title')
    cover = models.ImageField(upload_to='imagenes/portadas/', default="imagenes/portadas/book-default.png",
                              verbose_name='cover')
    description = models.CharField(max_length=100, verbose_name='description', null=True, blank=True)
    route = models.SlugField(max_length=255, unique=True, null=False, default='')

    # many to many field
    tag = models.ManyToManyField(Tag, blank=True)

    def get_portada(self):
        return self.cover.name

    def del_portada(self, to_delete):
        if to_delete != 'imagenes/portadas/book-default.png':
            self.cover.storage.delete(to_delete)

    # Override methods
    def save(self, *args, **kwargs):
        self.route = slugify(self.title)
        super(Story, self).save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        if self.cover.name != 'imagenes/portadas/book-default.png':
            self.cover.storage.delete(self.cover.name)
        super().delete()

    def __str__(self):
        return f'id: {self.id} | titulo: {self.title[:5]}...'
# -------- -------- -------- --------


# Página
class Page(models.Model):
    class Meta:
        db_table = prefix + 'story_page'

    # keys
    id = models.AutoField(primary_key=True)
    story = models.ForeignKey(Story, on_delete=models.CASCADE, null=True)
    # fields
    #texto = models.CharField(max_length=800, verbose_name='texto')

    def __str__(self) -> str:
        return f'id: {self.id} | pertenece: {self.story}'
# -------- -------- -------- --------


# Diálogo
class Dialogue(models.Model):
    class Meta:
        db_table = prefix + 'page_dialogue'

    # keys
    id = models.AutoField(primary_key=True)
    page = models.ForeignKey(Page, on_delete=models.CASCADE, null=True)
    # fields
    name = models.CharField(max_length=30, verbose_name='name')
    content = models.CharField(max_length=255, verbose_name='content')
    translation = models.CharField(max_length=255, verbose_name='translation')

    def __str__(self) -> str:
        return f'id: {self.id} | bt: {self.page}'
# -------- -------- -------- --------


# Repetir frase
class RepeatPhrase(models.Model):
    class Meta:
        db_table = prefix + 'page_repeat_phrase'

    # keys
    id = models.AutoField(primary_key=True)
    page = models.ForeignKey(Page, on_delete=models.CASCADE, null=True)
    # fields
    content = models.CharField(max_length=255, verbose_name='content')
    translation = models.CharField(max_length=255, verbose_name='translation')

    def __str__(self) -> str:
        return f'id: {self.id} | bt: {self.page}'
# -------- -------- -------- --------


# Pregunta y respuestas de opción múltiple
class Question(models.Model):
    class Meta:
        db_table = prefix + 'page_question'

    # keys
    id = models.AutoField(primary_key=True)
    page = models.ForeignKey(Page, on_delete=models.CASCADE, null=True)
    # fields
    question = models.CharField(max_length=255, verbose_name='question')

    def __str__(self) -> str:
        return f'q: {self.question[:5]}... | bt: {self.page}'


class Option(models.Model):
    class Meta:
        db_table = prefix + 'page_question_option'

    # keys
    id = models.AutoField(primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    # fields
    answer = models.CharField(max_length=255, verbose_name='answer')
    correct = models.BooleanField(default=False, null=False)

    def __str__(self) -> str:
        return f'ans: {self.answer[:5]}... = {self.correct} | bt: {self.question}'
# -------- -------- -------- --------
