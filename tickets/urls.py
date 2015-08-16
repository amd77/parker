# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views as v
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    url(r'^$', csrf_exempt(v.TicketFormView.as_view()), name="inicio"),
    url(r'^api/create$', csrf_exempt(v.CreatePost.as_view()), name="ticket_create"),
    url(r'^api/update$', csrf_exempt(v.UpdatePost.as_view()), name="ticket_update"),
    url(r'^dentro/$', v.EntradaTodayList.as_view(), name="dentro_today"),
    url(r'^dentro/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)$', v.EntradaDayList.as_view(), name="dentro_day"),
    url(r'^fuera/$', v.SalidaTodayList.as_view(), name="fuera_today"),
    url(r'^fuera/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)$', v.SalidaDayList.as_view(), name="fuera_day"),
    url(r'^fuera/(?P<year>\d+)/(?P<month>\d+)/$', v.SalidaMonthList.as_view(), name="fuera_month"),
    url(r'^fuera/(?P<year>\d+)/$', v.SalidaYearList.as_view(), name="fuera_year"),
]
