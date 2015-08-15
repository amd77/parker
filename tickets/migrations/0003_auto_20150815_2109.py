# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0002_entrada_fecha_post'),
    ]

    operations = [
        migrations.RenameField(
            model_name='salida',
            old_name='registro',
            new_name='entrada',
        ),
    ]
