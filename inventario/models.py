# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.apps import apps
from empresa.models import Empresa
import json
import os
import tempfile
import datetime
import requests


class Parking(models.Model):
    empresa = models.OneToOneField(Empresa)
    nombre = models.CharField(max_length=40)
    plazas = models.IntegerField()

    def __unicode__(self):
        return "{} ({})".format(self.nombre, self.empresa)

    def tupla_tarifa(self):
        "Obtener un tarifario dada una recta definida por puntos"
        # creamos una lista de listas
        lista = map(list, self.tarifa_set.values_list('precio', 'hora'))
        # agregamos el rango final de tiempo sacado de la siguiente linea
        n = len(lista)
        for i in range(n-1):
            lista[i].append(lista[i+1][1])
        # el rango final ponemos que es 24h
        lista[n-1].append(datetime.timedelta(days=1))
        # devolvemos [precio, hora_start, hora_end_no_inclusive]
        return lista

    def tabla_tarifa(self):
        "Tarifario con hh:mm para visualizar"
        for precio, min0, min1 in self.tupla_tarifa():
            t = min1 - datetime.timedelta(seconds=1)
            yield min0, t, precio

    def get_dia(self):
        return float(self.tarifa_set.last().precio)

    def get_tarifa(self, td):
        "Obtener una tarifa del tarifario"
        # calculo de dias completos
        precio_dias = td.days * self.get_dia()
        # calculo de la fraccion de dia
        td = datetime.timedelta(seconds=td.seconds)
        for precio, min0, min1 in self.tupla_tarifa():
            if min0 <= td < min1:
                return precio_dias + float(precio)

    def barreras_entrada(self):
        return self.barrera_set.filter(entrada=True)

    def barreras_salida(self):
        return self.barrera_set.filter(entrada=False)

    @property
    def entrada_set(self):
        Entrada = apps.get_model('tickets.Entrada')
        return Entrada.objects.por_parking(self)

    @property
    def coches_hoy(self):
        return self.entrada_set.de_hoy().count()

    @property
    def coches_dentro(self):
        return self.entrada_set.de_hoy().dentro().count()


class Expendedor(models.Model):
    parking = models.ForeignKey(Parking)
    nombre = models.CharField(max_length=40)
    mac = models.CharField(max_length=17)
    camera_command = models.CharField(max_length=255, blank=True, null=True, help_text="Comando para la camara, "
                                      "con {} donde queramos poner el output filename")

    def saca_foto(self):
        contenido = None
        if self.camera_command:
            filename = tempfile.mktemp()
            ret = os.system(self.camera_command.format(filename))
            if ret == 0:
                contenido = open(filename).read()
            if os.path.isfile(filename):
                os.unlink(filename)
        return contenido

    def __unicode__(self):
        return "{} de {}".format(self.nombre, self.parking.nombre)

    class Meta:
        verbose_name = 'expendedor'
        verbose_name_plural = 'expendedores'


class Barrera(models.Model):
    parking = models.ForeignKey(Parking)
    nombre = models.CharField(max_length=40)
    slug = models.CharField(max_length=40, unique=True)
    entrada = models.BooleanField()
    abre_url = models.URLField(max_length=100, blank=True, null=True, help_text="si hay url es que esta activo")
    abre_post = models.CharField(max_length=100, blank=True, null=True, help_text="post data en formato json")
    abresiempre_url = models.URLField(max_length=100, blank=True, null=True, help_text="si hay url es que esta activo")
    abresiempre_post = models.CharField(max_length=100, blank=True, null=True, help_text="post data en formato json")
    cierra_url = models.URLField(max_length=100, blank=True, null=True, help_text="si hay url es que esta activo")
    cierra_post = models.CharField(max_length=100, blank=True, null=True, help_text="post data en formato json")

    def abre(self):
        if self.abre_post:
            r = requests.post(self.abre_url, data=json.loads(self.abre_post))
        else:
            r = requests.get(self.abre_url)
        return r.status_code == 200

    def abresiempre(self):
        if self.abresiempre_post:
            r = requests.post(self.abresiempre_url, data=json.loads(self.abresiempre_post))
        else:
            r = requests.get(self.abresiempre_url)
        return r.status_code == 200

    def cierra(self):
        if self.cierra_post:
            r = requests.post(self.cierra_url, data=json.loads(self.cierra_post))
        else:
            r = requests.get(self.cierra_url)
        return r.status_code == 200

    def __unicode__(self):
        return "{} ({} de {})".format(self.slug, "entrada" if self.entrada else "salida", self.parking.nombre)

    class Meta:
        verbose_name = 'barrera'
        verbose_name_plural = 'barreras'


class Tarifa(models.Model):
    parking = models.ForeignKey(Parking)
    precio = models.DecimalField(max_digits=5, decimal_places=2)
    hora = models.DurationField(help_text="hora a partir de la cual aplica este precio")

    def __unicode__(self):
        return "{} = {:.2f} €".format(self.hora, self.precio)

    class Meta:
        ordering = ('hora', )


# from django.db.models.signals import pre_save
# from django.dispatch import receiver
# @receiver(pre_save, sender=Tarifa)
# def anula_date(sender, instance, using, **kwargs):
#     if isinstance(instance, datetime.datetime):
#         instance.hora = instance.hora.replace(year=1970, month=1, day=1)
