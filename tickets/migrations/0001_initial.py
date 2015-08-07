# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('empresa', '0001_initial'),
        ('inventario', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entrada',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo', models.CharField(help_text='Barcode EAN-13', unique=True, max_length=13)),
                ('fecha_solicitud', models.DateTimeField()),
                ('fecha_apertura', models.DateTimeField(null=True, blank=True)),
                ('fecha_cierre', models.DateTimeField(null=True, blank=True)),
                ('expendedor', models.ForeignKey(to='inventario.Expendedor')),
            ],
        ),
        migrations.CreateModel(
            name='Salida',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateTimeField()),
                ('minutos', models.FloatField()),
                ('euros', models.FloatField()),
                ('abonado', models.ForeignKey(blank=True, to='empresa.Abonado', null=True)),
                ('factura', models.ForeignKey(blank=True, to='empresa.Factura', null=True)),
                ('operario', models.ForeignKey(to='empresa.Operario')),
                ('registro', models.OneToOneField(to='tickets.Entrada')),
            ],
        ),
    ]
