# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0004_auto_20151213_1538'),
    ]

    operations = [
        migrations.CreateModel(
            name='Barrera',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=40)),
                ('slug', models.CharField(unique=True, max_length=40)),
                ('entrada', models.BooleanField()),
                ('abre_url', models.URLField(help_text='si hay url es que esta activo', max_length=40, null=True, blank=True)),
                ('abre_post', models.CharField(help_text='post data en formato json', max_length=40, null=True, blank=True)),
                ('abresiempre_url', models.URLField(help_text='si hay url es que esta activo', max_length=40, null=True, blank=True)),
                ('abresiempre_post', models.CharField(help_text='post data en formato json', max_length=40, null=True, blank=True)),
                ('cierra_url', models.URLField(help_text='si hay url es que esta activo', max_length=40, null=True, blank=True)),
                ('cierra_post', models.CharField(help_text='post data en formato json', max_length=40, null=True, blank=True)),
                ('parking', models.ForeignKey(to='inventario.Parking')),
            ],
            options={
                'verbose_name': 'barrera',
                'verbose_name_plural': 'barreras',
            },
        ),
    ]
