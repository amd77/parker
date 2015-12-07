# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0005_salida_fecha_caja'),
    ]

    operations = [
        migrations.AddField(
            model_name='entrada',
            name='foto',
            field=models.ImageField(null=True, upload_to='fotos/%Y/%m/%d', blank=True),
        ),
    ]
