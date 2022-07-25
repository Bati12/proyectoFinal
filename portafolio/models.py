from pickle import TRUE
from time import timezone
from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Portafolio(models.Model):
    titulo = models.CharField(max_length=150)
    descripcion = models.CharField(max_length=350)
    imagen = models.ImageField(upload_to='portafolio/images/')
    urlGit = models.URLField(blank=True)

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    titulo = models.CharField(max_length=150)
    descripcion = models.TextField()
    fecha = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user.username}:{self.titulo}'

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    imagen = models.ImageField(default='default.png')

    def __str__(self):
        return f'Perfil de {self.user.username}'