# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0002_auto_20151104_2151'),
    ]

    operations = [
        migrations.AddField(
            model_name='expendedor',
            name='camera_command',
            field=models.CharField(help_text='Comando para la camara, con {} donde queramos poner el output filename', max_length=255, null=True, blank=True),
        ),
    ]
