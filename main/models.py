from cProfile import label
from contextlib import nullcontext
from email.policy import default
from tabnanny import verbose
from django.db import models
from django.utils.text import slugify

prefix = 'app_'


class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField('username', max_length=50)
    password = models.CharField('password', max_length=150)

    def __str__(self) -> str:
        return f'id: {self.id}\nusername: {self.username}\npassword: {self.password}'


# Categoría
class Categoria(models.Model):
    class Meta:
        db_table = prefix + 'categoria'

    # keys
    id = models.AutoField(primary_key=True)
    # fields
    nombre = models.CharField(max_length=100, verbose_name='nombre')

    def __str__(self) -> str:
        return self.nombre


# -------- -------- -------- --------


# Historia
class Historia(models.Model):
    class Meta:
        db_table = prefix + 'historia'

    # primary key
    id = models.AutoField(primary_key=True)
    # fields
    titulo = models.CharField(max_length=100, verbose_name='titulo')
    portada = models.ImageField(upload_to='imagenes/portadas/', default="imagenes/portadas/book-default.png",
                                verbose_name='portada')
    descripcion = models.CharField(max_length=100, verbose_name='descripcion', null=True, blank=True)
    route = models.SlugField(max_length=255, unique=True, null=True, default='')

    # many to many field
    id_categoria = models.ManyToManyField(Categoria, blank=True)

    def get_portada(self):
        return self.portada.name

    def del_portada(self, borrar):
        if borrar != 'imagenes/portadas/book-default.png':
            self.portada.storage.delete(borrar)

    # Override methods
    def save(self, *args, **kwargs):
        if not self.route:
            self.route = slugify(self.titulo)
        super(Historia, self).save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        if self.portada.name != 'imagenes/portadas/book-default.png':
            self.portada.storage.delete(self.portada.name)
        super().delete()

    def __str__(self):
        return f'id: {self.id} | titulo: {self.titulo[:5]}...'


# -------- -------- -------- --------


# Página
class Page(models.Model):
    class Meta:
        db_table = prefix + 'historia_pagina'

    # keys
    id = models.AutoField(primary_key=True)
    historia = models.ForeignKey(Historia, on_delete=models.CASCADE, null=True)
    # fields
    texto = models.CharField(max_length=800, verbose_name='texto')

    def __str__(self) -> str:
        return f'id: {self.id} | texto: {self.texto[:5]}... | pertenece: {self.historia}'


# -------- -------- -------- --------


# Diálogo
class Dialogue(models.Model):
    class Meta:
        db_table = prefix + 'pag_conversation'

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
        db_table = prefix + 'pag_repeat_phrase'

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
        db_table = prefix + 'pag_question'

    # keys
    id = models.AutoField(primary_key=True)
    page = models.ForeignKey(Page, on_delete=models.CASCADE, null=True)
    # fields
    question = models.CharField(max_length=255, verbose_name='question')

    def __str__(self) -> str:
        return f'q: {self.question[:5]}... | bt: {self.page}'


class Option(models.Model):
    class Meta:
        db_table = prefix + 'pag_question_option'

    # keys
    id = models.AutoField(primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    # fields
    answer = models.CharField(max_length=255, verbose_name='answer')
    correct = models.BooleanField(default=False, null=False)

    def __str__(self) -> str:
        return f'ans: {self.answer[:5]}... = {self.correct} | bt: {self.question}'
# -------- -------- -------- --------
