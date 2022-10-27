from cProfile import label
from contextlib import nullcontext
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

    def __str__(self):
	    return self.nombre.capitalize()



class Historia(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=100, verbose_name='titulo')
    portada = models.ImageField(upload_to='imagenes/portadas/', default="imagenes/portadas/book-default.png", verbose_name='portada')
    descripcion = models.CharField(max_length=100, verbose_name='descripcion', null=True, blank=True)
    ruta = models.CharField(max_length=100, verbose_name='ruta', null=True)
    id_categoria = models.ManyToManyField(Categoria, blank=True)

    def delete(self, using=None, keep_parents=False):
        if self.portada.name != 'imagenes/portadas/book-default.png':
            self.portada.storage.delete(self.portada.name)
        super().delete()
    
    def get_portada(self):
        return self.portada.name

    def del_portada(self, borrar):
        if borrar != 'imagenes/portadas/book-default.png':
            self.portada.storage.delete(borrar)
    
    def limpiarRuta(self, route):
        route = route.lower().replace(' ', '-').replace('\\', '')
        route = route.replace('á', 'a').replace('é', 'e').replace('í', 'i')
        route = route.replace('ó', 'o').replace('ú', 'u')
        return route


    def __str__(self):
        return f'{self.titulo}'
    

class Pagina(models.Model):
    id = models.AutoField(primary_key=True)
    texto = models.CharField(max_length=800, verbose_name='texto')
    # para agregar páginas a una historia
    historia = models.ForeignKey(Historia, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.texto

    