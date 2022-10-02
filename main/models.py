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
    portada = models.ImageField(upload_to='imagenes/portadas/', verbose_name='portada', null=True)
    descripcion = models.CharField(max_length=100, verbose_name='descripcion', null=True)

    def delete(self, using=None, keep_parents=False):
        self.portada.storage.delete(self.portada.name)
        super().delete()
    
    def get_portada(self):
        return self.portada.name

    def del_portada(self, borrar):
        self.portada.storage.delete(borrar)
        


class CategoriaDeHistoria(models.Model):
    id = models.AutoField(primary_key=True)
    id_historia = models.IntegerField(verbose_name='id_historia')
    id_categoria = models.IntegerField(verbose_name='id_categoria')
