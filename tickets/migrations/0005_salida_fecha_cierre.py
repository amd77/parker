# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0004_auto_20150815_2131'),
    ]

    operations = [
        migrations.AddField(
            model_name='salida',
            name='fecha_cierre',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
