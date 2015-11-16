# -*- coding: utf-8 -*-

from django.db import models

import re
import uuid

from django.core import validators
from django.utils import timezone
from django.core.mail import send_mail
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django import forms

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
    nescesita = models.ForeignKey(Workers)

    def __str__(self):
        return self.nombre

class MyUser(AbstractBaseUser):

    email = models.EmailField('email address', unique=True, db_index=True, default="")
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    trabajo = models.ForeignKey(Jobs)
    idioma = models.ForeignKey(Idioma)
    lenguaje = models.ForeignKey(Lenguaje)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['trabajo','idioma','lenguaje','email']

