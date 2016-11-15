# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0009_remove_salida_minutos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salida',
            name='duracion',
            field=models.DurationField(null=True, blank=True),
        ),
    ]
