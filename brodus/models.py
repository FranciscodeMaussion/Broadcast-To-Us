# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Lenguaje(models.Model):
    class Meta:
        verbose_name = "Lenguaje de programación"
        verbose_name_plural = "Lenguajes de programación"

    nombre = models.CharField(u'Nombre', max_length=200)

    def __str__(self):
        return self.nombre

class Idioma(models.Model):
    class Meta:
        verbose_name = "Idioma"
        verbose_name_plural = "Idiomas"

    nombre = models.CharField(u'Nombre', max_length=200)

    def __str__(self):
        return self.nombre

class Jobs(models.Model):
    class Meta:
        verbose_name = "Trabajo"
        verbose_name_plural = "Trabajos"

    nombre = models.CharField(u'Nombre', max_length=200)
    desc = models.CharField(u'Descripción', max_length=400)

    def __str__(self):
        return self.nombre

class Workers(models.Model):
    class Meta:
        verbose_name = "Trabajador"
        verbose_name_plural = "Trabajadores"

    tipo = models.ForeignKey(Jobs)
    cantidad = models.IntegerField(u'Cantidad', default=0)

    def __str__(self):
        return tipo.nombre

class Proj(models.Model):
    class Meta:
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"

    nombre = models.CharField(u'Nombre', max_length=200)
    desc = models.CharField(u'Descripción', max_length=400)
    nescesita_w = models.ForeignKey(Workers, default=None, blank=True, null=True)
    nescesita_i = models.ForeignKey(Jobs, default=None, blank=True, null=True)
    nescesita_l = models.ForeignKey(Lenguaje, default=None, blank=True, null=True)
    owner = models.ForeignKey(User, default=None)

    def __str__(self):
        return self.nombre

class Rol(models.Model):
    class Meta:
        verbose_name = "Rol"
        verbose_name_plural = "Roles"

    trabajo = models.ForeignKey(Jobs)
    idioma = models.ForeignKey(Idioma)
    lenguaje = models.ForeignKey(Lenguaje)
    user = models.OneToOneField(User, related_name="persona", default=None)

    def __str__(self):
        return self.nombre
