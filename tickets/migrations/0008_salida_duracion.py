# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

import datetime


def forwards(apps, schema_editor):
    Salida = apps.get_model('tickets', 'Salida')
    for s in Salida.objects.all():
        days = int(s.minutos / (24 * 60))
        seconds = int(s.minutos * 60) % (24 * 60 * 60)
        s.duracion = datetime.timedelta(days=days, seconds=seconds)
        s.save()


def backwards(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0007_salida_perdido'),
    ]

    operations = [
        migrations.AddField(
            model_name='salida',
            name='duracion',
            field=models.DurationField(default=datetime.timedelta(0)),
            preserve_default=False,
        ),
        migrations.RunPython(forwards, backwards),
    ]
