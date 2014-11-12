# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from registro.models import Registro
from django.utils import timezone


class Command(BaseCommand):
    help = u'Mete lo siguiente en base de datos: [entrar|salir] [matricula]'

    def handle(self, *args, **kwargs):
        if len(args) < 2:
            print u"Linea de comandos:"
            print u"- entra matricula:     e matricula [usuario]"
            print u"- sale matricula:      s matricula [usuario]"
            print u"- modifica matricula:  r matricula1 matricula2 (solo los que estan dentro)"
            return
        command_line = u" ".join([x.decode("utf-8") for x in args])
        comando = matricula = usuario = None
        args = list(args)
        try:
            comando = args.pop(0).lower().strip()
            matricula = args.pop(0).lower().strip()
            usuario = args.pop(0).lower().strip()
        except IndexError:
            pass
        if comando == "e":
            out = Registro.matricula_entra(matricula, usuario)
        elif comando == "s":
            out = Registro.matricula_sale(matricula, usuario)
        # elif comando == "r":
        #     out = Registro.matricula_renombra(matricula, matricula)
        else:
            out = u"Comando '{}' no reconocido".format(comando)
        print out.encode("utf-8")
        msg = u"{} [{}] {}\n".format(timezone.now(), command_line, out)
        file("parker.log", "a").write(msg.encode("utf-8"))
