# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0003_auto_20150815_2109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salida',
            name='euros',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
