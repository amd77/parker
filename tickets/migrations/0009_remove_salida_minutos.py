# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0008_salida_duracion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salida',
            name='minutos',
        ),
    ]
