# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from empresa.models import Empresa


def _bressenham(x0, y0, x1, y1):
    # http://rosettacode.org/wiki/Bitmap/Bresenham%27s_line_algorithm#Python
    # con el yield cambiado de sitio para que no repita puntos
    dx = float(abs(x1-x0))
    dy = float(abs(y1-y0))
    x, y = x0, y0
    sx = -1 if x0 > x1 else 1
    sy = -1 if y0 > y1 else 1
    if dx > dy:
        err = dx / 2.0
        while x != x1:
            err -= dy
            if err < 0:
                yield (x, y)
                y += sy
                err += dx
            x += sx
    else:
        err = dy / 2.0
        while y != y1:
            err -= dx
            if err < 0:
                yield (x, y)
                x += sx
                err += dy
            y += sy


def _hhmm(minutos):
    "Conversion de minutos a HH:MM"
    minutos = int(minutos)
    return "{:02d}:{:02d}".format(minutos / 60, minutos % 60)


class Parking(models.Model):
    empresa = models.OneToOneField(Empresa)
    nombre = models.CharField(max_length=40)
    plazas = models.IntegerField()

    def __unicode__(self):
        return "{} ({})".format(self.nombre, self.empresa)

    def tupla_tarifa(self):
        "Obtener un tarifario dada una recta definida por puntos"
        lista = list(self.tarifa_set.all())
        actual = lista[0]
        for siguiente in lista[1:]:
            x0, y0 = actual.minutos, actual.precio
            dx, dy = actual.salto_minutos, actual.salto_precio
            x1 = int(round((siguiente.minutos - x0)/dx))
            y1 = int(round((siguiente.precio - y0)/dy))
            for i, j in _bressenham(0, 0, x1, y1):
                min0 = i*dx + x0
                min1 = min0 + dx - 1
                precio = j * dy + y0
                yield (min0, min1, precio)
            actual = siguiente

    def tabla_tarifa(self):
        "Tarifario con hh:mm para visualizar"
        for min0, min1, precio in self.tupla_tarifa():
            yield (_hhmm(min0), _hhmm(min1), precio)

    def get_tarifa(self, minutos):
        "Obtener una tarifa del tarifario"
        for min0, min1, precio in self.tupla_tarifa():
            if min0 <= minutos <= min1:
                return precio


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
        return "{} = {:.2f} €".format(_hhmm(self.minutos), self.precio)
