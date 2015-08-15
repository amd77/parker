# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from empresa.models import Operario, Abonado, Factura
from inventario.models import Expendedor
# import datetime

TZ = timezone.get_default_timezone()


class Entrada(models.Model):
    "Esto es la emision de un ticket en una expendedora"
    codigo = models.CharField(max_length=13, help_text="Barcode EAN-13", unique=True)
    expendedor = models.ForeignKey(Expendedor)
    fecha_post = models.DateTimeField(auto_now_add=True)
    fecha_solicitud = models.DateTimeField()
    fecha_apertura = models.DateTimeField(blank=True, null=True)
    fecha_cierre = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return "{} ({})".format(self.codigo, self.expendedor)


class Salida(models.Model):
    "Recogida de un ticket en salida, con sus datos de cobro y factura si pide"
    entrada = models.OneToOneField(Entrada)
    fecha = models.DateTimeField()
    minutos = models.FloatField()
    euros = models.FloatField()
    operario = models.ForeignKey(Operario)
    abonado = models.ForeignKey(Abonado, blank=True, null=True)
    factura = models.ForeignKey(Factura, blank=True, null=True)

    def __unicode__(self):
        return "{} ({} minutos) por {}".format(self.fecha, self.minutos, self.operario.user.username)
