# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from empresa.models import Operario, Abonado, Factura
from inventario.models import Expendedor, _hhmm
# import datetime

TZ = timezone.get_default_timezone()


class EntradaQuerySet(models.QuerySet):
    def de_hoy(self):
        now = timezone.now()
        inicio = now.replace(hour=0, minute=0, second=0, microsecond=0)
        fin = now.replace(hour=23, minute=59, second=59, microsecond=999999)
        return self.filter(fecha_post__gt=inicio, fecha_post__lt=fin)

    def por_parking(self, parking):
        return self.filter(expendedor__parking=parking)

    def por_operario(self, operario):
        return self.filter(operario=operario)

    def dentro(self):
        return self.exclude(fecha_apertura__isnull=False).exclude(fecha_cierre__isnull=False)


class Entrada(models.Model):
    "Esto es la emision de un ticket en una expendedora"
    codigo = models.CharField(max_length=13, help_text="Barcode EAN-13", unique=True)
    expendedor = models.ForeignKey(Expendedor)
    fecha_post = models.DateTimeField(auto_now_add=True)
    fecha_solicitud = models.DateTimeField()
    fecha_apertura = models.DateTimeField(blank=True, null=True)
    fecha_cierre = models.DateTimeField(blank=True, null=True)

    objects = EntradaQuerySet.as_manager()

    @property
    def fecha(self):
        return self.fecha_cierre or self.fecha_apertura or \
            self.fecha_solicitud or self.fecha_post

    def __unicode__(self):
        return "{} ({})".format(self.codigo, self.expendedor)


class SalidaQuerySet(models.QuerySet):
    def de_hoy(self):
        now = timezone.now()
        inicio = now.replace(hour=0, minute=0, second=0, microsecond=0)
        fin = now.replace(hour=23, minute=59, second=59, microsecond=999999)
        return self.filter(fecha__gt=inicio, fecha__lt=fin)

    def por_parking(self, parking):
        return self.filter(expendedor__parking=parking)

    def por_operario(self, operario):
        return self.filter(operario=operario)

    def sin_cerrar(self):
        return self.filter(fecha_caja__isnull=True)


class Salida(models.Model):
    "Recogida de un ticket en salida, con sus datos de cobro y factura si pide"
    entrada = models.OneToOneField(Entrada)
    fecha = models.DateTimeField()
    minutos = models.FloatField()
    euros = models.FloatField(blank=True, null=True)
    operario = models.ForeignKey(Operario)
    abonado = models.ForeignKey(Abonado, blank=True, null=True)
    factura = models.ForeignKey(Factura, blank=True, null=True)
    fecha_caja = models.DateTimeField(blank=True, null=True)

    objects = SalidaQuerySet.as_manager()

    def __unicode__(self):
        return "{} ({} minutos) por {}".format(self.fecha, self.minutos, self.operario.user.username)

    def minutos_str(self):
        return _hhmm(self.minutos)

    def fecha_salida_str(self):
        if self.fecha.date() == self.entrada.fecha.date():
            return self.fecha.time()
        else:
            return self.fecha

    def fecha_entrada_str(self):
        if self.fecha.date() == self.entrada.fecha.date():
            return self.entrada.fecha.time()
        else:
            return self.entrada.fecha

    @staticmethod
    def crea_por_entrada(entrada, operario):
        try:
            return False, entrada.salida
        except AttributeError:
            pass
        fecha = timezone.now()
        minutos = (fecha - entrada.fecha).total_seconds() / 60.0
        euros = entrada.expendedor.parking.get_tarifa(minutos)
        return True, Salida.objects.create(entrada=entrada, fecha=fecha,
                                           minutos=minutos, euros=euros,
                                           operario=operario)
