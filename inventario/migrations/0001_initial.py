# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('empresa', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Expendedor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=40)),
                ('mac', models.CharField(max_length=17)),
            ],
            options={
                'verbose_name': 'expendedor',
                'verbose_name_plural': 'expendedores',
            },
        ),
        migrations.CreateModel(
            name='Parking',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=40)),
                ('plazas', models.IntegerField()),
                ('empresa', models.OneToOneField(to='empresa.Empresa')),
            ],
        ),
        migrations.CreateModel(
            name='Tarifa',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('minutos', models.IntegerField()),
                ('precio', models.DecimalField(max_digits=5, decimal_places=2)),
                ('salto_minutos', models.IntegerField(default=10)),
                ('salto_precio', models.DecimalField(default='0.1', max_digits=5, decimal_places=2)),
                ('parking', models.ForeignKey(to='inventario.Parking')),
            ],
        ),
        migrations.AddField(
            model_name='expendedor',
            name='parking',
            field=models.ForeignKey(to='inventario.Parking'),
        ),
    ]
