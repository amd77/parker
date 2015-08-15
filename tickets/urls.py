# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views as v
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    url(r'^$', csrf_exempt(v.TicketFormView.as_view()), name="inicio"),
    url(r'^api/create$', csrf_exempt(v.Create.as_view()), name="ticket_create"),
]
