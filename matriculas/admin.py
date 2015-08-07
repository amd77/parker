# -*- coding: utf-8 -*-

from django.contrib import admin
admin.autodiscover()

from .models import Registro
admin.site.register(Registro)
