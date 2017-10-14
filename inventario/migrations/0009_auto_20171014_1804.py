# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0008_nodoremoto_host_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nodoremoto',
            name='url',
            field=models.CharField(help_text=' url del demonio nameko', max_length=100, null=True, blank=True),
        ),
    ]
