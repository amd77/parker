# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views as v
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    url(r'^$', csrf_exempt(v.TicketFormView.as_view()), name="inicio"),
    url(r'^api/create$', csrf_exempt(v.CreatePost.as_view()), name="ticket_create"),
    url(r'^api/update$', csrf_exempt(v.UpdatePost.as_view()), name="ticket_update"),
    url(r'^cierre$', v.CierreView.as_view(), name="ticket_cierre"),
    url(r'^fotos/(?P<cuales>\w*)$', v.FotoToday.as_view(), name="fotos_today"),
    url(r'^estadisticas/entrada/$', v.EntradaTodayList.as_view(), name="estadisticas_entrada_today"),
    url(r'^estadisticas/entrada/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<cuales>\w*)$', v.EntradaDayList.as_view(), name="estadisticas_entrada_day"),
    url(r'^estadisticas/entrada/(?P<year>\d+)/(?P<month>\d+)/(?P<cuales>\w*)$', v.EntradaMonthList.as_view(), name="estadisticas_entrada_month"),
    url(r'^estadisticas/salida/$', v.SalidaTodayList.as_view(), name="estadisticas_salida_today"),
    url(r'^estadisticas/salida/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<cuales>\w*)$', v.SalidaDayList.as_view(), name="estadisticas_salida_day"),
    url(r'^estadisticas/salida/(?P<year>\d+)/(?P<month>\d+)/(?P<cuales>\w*)$', v.SalidaMonthList.as_view(), name="estadisticas_salida_month"),
]
