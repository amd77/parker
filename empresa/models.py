# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# import datetime

TZ = timezone.get_default_timezone()


class Empresa(models.Model):
    nombre = models.CharField(max_length=120)
    cif = models.CharField(max_length=12)
    direccion = models.TextField()
    ultima_factura = models.IntegerField(default="20150001")

    def __unicode__(self):
        return self.nombre


class Operario(models.Model):
    empresa = models.ForeignKey(Empresa)
    user = models.OneToOneField(User)
    es_administrador = models.BooleanField(default=False)
    direccion_ip = models.GenericIPAddressField(
        blank=True, null=True,
        help_text="Direccion IP del usuario al iniciar sesión y usada para saber dónde está la impresora")

    def __unicode__(self):
        return "{} de {}".format(self.user.username, self.empresa.nombre)

    @property
    def coches_facturados_hoy(self):
        return self.salida_set.de_hoy().count()

class Abonado(models.Model):
    empresa = models.ForeignKey(Empresa)
    nombre = models.CharField(max_length=120)
    codigo = models.CharField(max_length=13, help_text="Barcode EAN-13", unique=True)

    def __unicode__(self):
        return self.nombre


class Factura(models.Model):
    "Documento factura que se imprime y se entrega opcionalmente al cliente"
    empresa = models.ForeignKey(Empresa)
    nombre = models.CharField(max_length=40)
    numero = models.IntegerField()
    fecha = models.DateField()
    concepto = models.TextField()
    importe = models.DecimalField(max_digits=5, decimal_places=2)
    igic = models.DecimalField(max_digits=5, decimal_places=2)
    total = models.DecimalField(max_digits=5, decimal_places=2)
