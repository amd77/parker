# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from . import views as v

urlpatterns = patterns(
    '',
    url(r'^tarifas$', v.Tarifas.as_view(), name="tarifas"),
)
