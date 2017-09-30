# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0005_barrera'),
    ]

    operations = [
        migrations.AlterField(
            model_name='barrera',
            name='abre_post',
            field=models.CharField(help_text='post data en formato json', max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='barrera',
            name='abre_url',
            field=models.URLField(help_text='si hay url es que esta activo', max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='barrera',
            name='abresiempre_post',
            field=models.CharField(help_text='post data en formato json', max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='barrera',
            name='abresiempre_url',
            field=models.URLField(help_text='si hay url es que esta activo', max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='barrera',
            name='cierra_post',
            field=models.CharField(help_text='post data en formato json', max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='barrera',
            name='cierra_url',
            field=models.URLField(help_text='si hay url es que esta activo', max_length=100, null=True, blank=True),
        ),
    ]
