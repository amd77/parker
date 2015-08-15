# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from . import views as v
from django.views.decorators.csrf import csrf_exempt

urlpatterns = patterns(
    '',
    url(r'^api/create$', csrf_exempt(v.Create.as_view()), name="ticket_create"),
)
