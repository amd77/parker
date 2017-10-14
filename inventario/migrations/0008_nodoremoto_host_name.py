# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0007_auto_20171014_1756'),
    ]

    operations = [
        migrations.AddField(
            model_name='nodoremoto',
            name='host_name',
            field=models.CharField(help_text='Nombre del Host', max_length=100, null=True, blank=True),
        ),
    ]
