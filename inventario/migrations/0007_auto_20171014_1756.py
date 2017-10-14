# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0006_auto_20170930_1629'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComandoRemoto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(help_text='nombre del comando', max_length=100, null=True, blank=True)),
                ('comando', models.CharField(help_text='comando', max_length=100, null=True, blank=True)),
            ],
            options={
                'verbose_name': 'comando Remoto',
                'verbose_name_plural': 'Comandos Remotos',
            },
        ),
        migrations.CreateModel(
            name='NodoRemoto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField(help_text=' url del demonio nameko', max_length=100, null=True, blank=True)),
                ('nombre', models.CharField(help_text='Nombre del demonio nameko', max_length=100, null=True, blank=True)),
                ('parking', models.ForeignKey(to='inventario.Parking')),
            ],
            options={
                'verbose_name': 'Nodo Remoto',
                'verbose_name_plural': 'Nodos Remotos',
            },
        ),
        migrations.AddField(
            model_name='comandoremoto',
            name='nodoremoto',
            field=models.ForeignKey(to='inventario.NodoRemoto'),
        ),
    ]
