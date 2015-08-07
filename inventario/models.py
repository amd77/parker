# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from empresa.models import Empresa


class Parking(models.Model):
    empresa = models.OneToOneField(Empresa)
    nombre = models.CharField(max_length=40)
    plazas = models.IntegerField()

    def __unicode__(self):
        return "{} ({})".format(self.nombre, self.empresa)


class Expendedor(models.Model):
    parking = models.ForeignKey(Parking)
    nombre = models.CharField(max_length=40)
    mac = models.CharField(max_length=17)

    def __unicode__(self):
        return "{} de {}".format(self.nombre, self.parking.nombre)

    class Meta:
        verbose_name = 'expendedor'
        verbose_name_plural = 'expendedores'


class Tarifa(models.Model):
    parking = models.ForeignKey(Parking)
    minutos = models.IntegerField()
    precio = models.DecimalField(max_digits=5, decimal_places=2)
    salto_minutos = models.IntegerField(default=10)
    salto_precio = models.DecimalField(max_digits=5, decimal_places=2, default='0.1')

    def __unicode__(self):
        return "{:.3f} eur/min".format(self.precio/self.minutos)
