from email.policy import default
from tabnanny import verbose
from django.db import models


class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField('username', max_length=50)
    password = models.CharField('password', max_length=150)

    def __str__(self) -> str:
        return f'id: {self.id}\nusername: {self.username}\npassword: {self.password}'


class Categoria(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, verbose_name='nombre')


class Historia(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=100, verbose_name='titulo')
    portada = models.ImageField(upload_to='imagenes/portadas/', default="imagenes/portadas/book-default.png", verbose_name='portada')
    descripcion = models.CharField(max_length=100, verbose_name='descripcion', null=True)
    id_categoria = models.ManyToManyField(Categoria)


    def delete(self, using=None, keep_parents=False):
        if self.portada.name != 'imagenes/portadas/book-default.png':
            self.portada.storage.delete(self.portada.name)
        super().delete()
    
    def get_portada(self):
        return self.portada.name

    def del_portada(self, borrar):
        if borrar != 'imagenes/portadas/book-default.png':
            self.portada.storage.delete(borrar)


    def __str__(self) -> str:
        return f'{self.id} {self.titulo}'
        
