#!/usr/bin/env python

import eventlet
eventlet.monkey_patch(thread=False)
# opcion thread=False sacada de
# https://github.com/benoitc/gunicorn/issues/927#issuecomment-102176547

from django.conf import settings
from django.core.management.base import BaseCommand
from inventario.models import Expendedor
from nameko.rpc import rpc
from nameko.runners import ServiceRunner
from tickets.models import Entrada
import signal


class MasterService(object):
    name = 'master'

    @rpc
    def create_ticket(self, mac, codigo, fecha_solicitud):
        try:
            exp = Expendedor.objects.get(mac=mac)
            obj = Entrada.objects.create(expendedor=exp, codigo=codigo,
                                         fecha_solicitud=fecha_solicitud)
            msg = "ok: {}".format(obj.pk)
            print obj, msg
        except Exception as e:
            msg = "ko: {}".format(e)
            print "ERROR", msg
        return msg

    @rpc
    def update_ticket(self, codigo, fecha_apertura=None, fecha_cierre=None):
        try:
            obj = Entrada.objects.get(codigo=codigo)
            if fecha_apertura:
                obj.fecha_apertura = fecha_apertura
            if fecha_cierre:
                obj.fecha_cierre = fecha_cierre
            obj.save()
            msg = "ok: {}".format(obj.pk)
            print obj, msg
        except Exception as e:
            msg = "ko: {}".format(e)
            print "ERROR", msg
        return msg


class Command(BaseCommand):
    help = "Ejecuta un nameko rpc server para trabajar con el orm de django"

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
