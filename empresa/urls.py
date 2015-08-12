# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from . import views as v

urlpatterns = patterns(
    '',
    url(r'^$', v.Panel.as_view(), name="inicio"),
)

