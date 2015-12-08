# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views as v
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    url(r'^$', csrf_exempt(v.TicketFormView.as_view()), name="inicio"),
    url(r'^api/create$', csrf_exempt(v.CreatePost.as_view()), name="ticket_create"),
    url(r'^api/update$', csrf_exempt(v.UpdatePost.as_view()), name="ticket_update"),
    url(r'^cierre$', v.CierreView.as_view(), name="ticket_cierre"),
    url(r'^fotos/$', v.FotoToday.as_view(), name="fotos_today"),
    url(r'^estadisticas/$', v.EntradaTodayList.as_view(), name="estadisticas_today"),
    url(r'^estadisticas/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)$', v.EntradaDayList.as_view(), name="estadisticas_day"),
    url(r'^estadisticas/(?P<year>\d+)/(?P<month>\d+)/$', v.EntradaMonthList.as_view(), name="estadisticas_month"),
    url(r'^estadisticas/(?P<year>\d+)/$', v.EntradaYearList.as_view(), name="estadisticas_year"),
]
