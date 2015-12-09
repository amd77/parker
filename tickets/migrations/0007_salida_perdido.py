# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0006_entrada_foto'),
    ]

    operations = [
        migrations.AddField(
            model_name='salida',
            name='perdido',
            field=models.BooleanField(default=False),
        ),
    ]
