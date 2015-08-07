# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Abonado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=120)),
                ('codigo', models.CharField(help_text='Barcode EAN-13', unique=True, max_length=13)),
            ],
        ),
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=120)),
                ('cif', models.CharField(max_length=12)),
                ('direccion', models.TextField()),
                ('ultima_factura', models.IntegerField(default='20150001')),
            ],
        ),
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=40)),
                ('numero', models.IntegerField()),
                ('fecha', models.DateField()),
                ('concepto', models.TextField()),
                ('importe', models.DecimalField(max_digits=5, decimal_places=2)),
                ('igic', models.DecimalField(max_digits=5, decimal_places=2)),
                ('total', models.DecimalField(max_digits=5, decimal_places=2)),
                ('empresa', models.ForeignKey(to='empresa.Empresa')),
            ],
        ),
        migrations.CreateModel(
            name='Operario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('es_administrador', models.BooleanField(default=False)),
                ('direccion_ip', models.GenericIPAddressField(help_text='Direccion IP del usuario al iniciar sesi\xf3n y usada para saber d\xf3nde est\xe1 la impresora', null=True, blank=True)),
                ('empresa', models.ForeignKey(to='empresa.Empresa')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='abonado',
            name='empresa',
            field=models.ForeignKey(to='empresa.Empresa'),
        ),
    ]
