#!/usr/bin/env python

import eventlet
eventlet.monkey_patch()

from django.conf import settings
from django.core.management.base import BaseCommand
from nameko.rpc import rpc
from nameko.runners import ServiceRunner
import requests
import signal


class MasterService(object):
    name = 'master'

    @rpc
    def create_ticket(self, mac, codigo, fecha_solicitud):
        url = "http://localhost:8000/parker/api/create"
        data = dict(mac=mac, codigo=codigo, fecha_solicitud=fecha_solicitud)
        r = requests.post(url, data=data)
        print url, data, r
        return r.text

    @rpc
    def update_ticket(self, codigo, fecha_apertura=None, fecha_cierre=None):
        url = "http://localhost:8000/parker/api/update"
        data = dict(codigo=codigo, fecha_apertura=fecha_apertura,
                    fecha_cierre=fecha_cierre)
        r = requests.post(url, data=data)
        print url, data, r
        return r.text


class Command(BaseCommand):
    help = "Ejecuta un nameko rpc server para postear a django"

    def handle(self, *args, **options):
        runner = ServiceRunner(settings.AMQP_CONFIG)
        runner.add_service(MasterService)

        def shutdown(signum, frame):
            eventlet.spawn_n(runner.kill)
        signal.signal(signal.SIGTERM, shutdown)

        runner.start()
        try:
            runner.wait()
        except KeyboardInterrupt:
            try:
                runner.stop()
            except KeyboardInterrupt:
                runner.kill()
