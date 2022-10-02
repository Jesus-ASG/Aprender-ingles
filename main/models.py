from django.db import models

class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField('username', max_length=50)
    password = models.CharField('password', max_length=150)

    def __str__(self) -> str:
        return f'id: {self.id}\nusername: {self.username}\npassword: {self.password}'


class Categorias(models.Model):
    id = models.AutoField(primary_key = True)
    nombre = models.CharField(max_length = 100, verbose_name='nombre')
    

