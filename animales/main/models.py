
from django.db import models

class Animal(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)
    genero = models.CharField(max_length=10)
    raza = models.CharField(max_length=100)
    edad = models.IntegerField()
    tamano = models.CharField(max_length=50)
    url_foto = models.URLField(max_length=200)
    url_detalle = models.URLField(max_length=200)

    def __str__(self):
        return self.nombre
