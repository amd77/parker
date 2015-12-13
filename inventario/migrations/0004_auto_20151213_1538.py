# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0003_expendedor_camera_command'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tarifa',
            options={'ordering': ('hora',)},
        ),
        migrations.RemoveField(
            model_name='tarifa',
            name='minutos',
        ),
        migrations.RemoveField(
            model_name='tarifa',
            name='salto_minutos',
        ),
        migrations.RemoveField(
            model_name='tarifa',
            name='salto_precio',
        ),
        migrations.AddField(
            model_name='tarifa',
            name='hora',
            field=models.DurationField(default=datetime.timedelta(seconds=0), help_text='hora a partir de la cual aplica este precio'),
            preserve_default=False,
        ),
    ]
