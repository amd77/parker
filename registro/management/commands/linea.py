# -*- coding: utf-8 -*-

from optparse import make_option
from django.core.management.base import BaseCommand
from django.conf import settings
from registro.models import Registro
from django.utils import timezone

class Command(BaseCommand):

    help = u'Mete lo siguiente en base de datos: [entrar|salir] [matricula]'

    def handle(self, *args, **kwargs):
        if len(args) < 2:
            print "Linea de comandos:"
            print "- entra matricula:     e matricula"
            print "- sale matricula:      s matricula"
            print "- modifica matricula:  r matricula1 matricula2 (solo los que estan dentro)"
            return
        comando = args[0].lower()
        matricula = args[1].lower().strip()
        if comando == "e":
            out = Registro.matricula_entra(matricula)
            if not out:
                print "ERROR matricula '{}' ya esta dentro!!".format(matricula)
            else:
                print "Entrando matricula '{}'".format(matricula)
        elif comando == "s":
            out = Registro.matricula_sale(matricula)
            if out:
                print "Saliendo matricula '{}'".format(matricula)
            else:
                print "ERROR matricula '{}' no esta dentro!!".format(matricula)

        elif comando == "r":
            out = Registro.matricula_renombra(matricula1, matricula2)
            if out:
                print "Renombrando matricula '{}'".format(matricula1)
            else:
                print "ERROR matricula '{}' no esta dentro!!".format(matricula1)
        else:
            print "Comando '{}' no reconocido".format(comando)



