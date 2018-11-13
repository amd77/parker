# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0009_auto_20171014_1804'),
    ]

    operations = [
        migrations.CreateModel(
            name='Visor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField(default='http://192.168.1.1:8000')),
                ('descripcion', models.CharField(default='visor colocado en ...', max_length=200)),
                ('parking', models.ForeignKey(to='inventario.Parking')),
            ],
            options={
                'verbose_name_plural': 'Visores',
            },
        ),
    ]
