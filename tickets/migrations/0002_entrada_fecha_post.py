# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='entrada',
            name='fecha_post',
            field=models.DateTimeField(default='2015-01-01 01:01:01Z', auto_now_add=True),
            preserve_default=False,
        ),
    ]
