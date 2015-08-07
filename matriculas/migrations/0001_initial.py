# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Registro',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('matricula', models.CharField(max_length=40)),
                ('fecha_entrada', models.DateTimeField(default=django.utils.timezone.now)),
                ('fecha_salida', models.DateTimeField(null=True, blank=True)),
                ('minutos', models.FloatField(null=True, blank=True)),
                ('euros', models.FloatField(null=True, blank=True)),
                ('usuario_entrada', models.CharField(max_length=40, null=True, blank=True)),
                ('usuario_salida', models.CharField(max_length=40, null=True, blank=True)),
                ('emitido_ticket', models.NullBooleanField()),
            ],
            options={
                'ordering': ['-fecha_entrada'],
            },
        ),
    ]
