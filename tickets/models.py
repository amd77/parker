# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from empresa.models import Operario, Abonado, Factura
from inventario.models import Expendedor
from django.db.models import Sum
import datetime


TZ = timezone.get_default_timezone()


class EntradaQuerySet(models.QuerySet):
    def de_hoy(self):
        return self.por_dia(timezone.now())

    def por_dia(self, now):
        inicio = now.replace(hour=0, minute=0, second=0, microsecond=0)
        fin = now.replace(hour=23, minute=59, second=59, microsecond=999999)
        return self.filter(fecha_post__range=(inicio, fin))

    def por_parking(self, parking):
        return self.filter(expendedor__parking=parking)

    def por_operario(self, operario):
        return self.filter(salida__operario=operario)

    def dentro(self):
        return self.filter(salida__isnull=True)

    def euros(self):
        return self.aggregate(out=Sum('salida__euros'))['out'] or 0.0


class Entrada(models.Model):
    "Esto es la emision de un ticket en una expendedora"
    codigo = models.CharField(max_length=13, help_text="Barcode EAN-13", unique=True)
    expendedor = models.ForeignKey(Expendedor)
    fecha_post = models.DateTimeField(auto_now_add=True)
    fecha_solicitud = models.DateTimeField()
    fecha_apertura = models.DateTimeField(blank=True, null=True)
    fecha_cierre = models.DateTimeField(blank=True, null=True)
    foto = models.ImageField(upload_to="fotos/%Y/%m/%d", blank=True, null=True)

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

    def euros(self):
        return self.aggregate(out=Sum('euros'))['out'] or 0.0


class Salida(models.Model):
    "Recogida de un ticket en salida, con sus datos de cobro y factura si pide"
    entrada = models.OneToOneField(Entrada)
    fecha = models.DateTimeField()
    duracion = models.DurationField(blank=True, null=True)
    euros = models.FloatField(blank=True, null=True)
    operario = models.ForeignKey(Operario)
    abonado = models.ForeignKey(Abonado, blank=True, null=True)
    factura = models.ForeignKey(Factura, blank=True, null=True)
    fecha_caja = models.DateTimeField(blank=True, null=True)
    perdido = models.BooleanField(default=False)

    objects = SalidaQuerySet.as_manager()

    def __unicode__(self):
        hora = self.fecha.strftime('%H:%M:%S')
        return "{} = {} (por {})".format(hora, self.duracion, self.operario.user.username)

    @staticmethod
    def crea_por_entrada(entrada, operario, abonado=None, perdido=False):
        try:
            return False, entrada.salida
        except AttributeError:
            pass
        fecha = timezone.now()
        duracion = fecha - entrada.fecha
        duracion = datetime.timedelta(days=duracion.days, seconds=duracion.seconds)  # quitar microseconds
        euros = entrada.expendedor.parking.get_tarifa(duracion) if not abonado else 0.0
        return True, Salida.objects.create(entrada=entrada, fecha=fecha,
                                           duracion=duracion, euros=euros,
                                           operario=operario, abonado=abonado,
                                           perdido=perdido)
