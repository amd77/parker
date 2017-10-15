# -*- coding: utf-8 -*-

from django.http import Http404
from django.views.generic import TemplateView, RedirectView
from empresa.views import OperarioMixin
from .models import Barrera, NodoRemoto, ComandoRemoto
from nameko.standalone.rpc import ClusterRpcProxy


class Tarifas(OperarioMixin, TemplateView):
    template_name = "inventario/tarifas.html"


class BarreraComando(OperarioMixin, RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        try:
            barrera = Barrera.objects.get(slug=self.kwargs['slug'])
        except Barrera.DoesNotExist:
            raise Http404("Barrera desconocida")
        comando = self.kwargs['comando']
        if comando == "abre":
            barrera.abre()
        elif comando == "abresiempre":
            barrera.abresiempre()
        elif comando == "cierra":
            barrera.cierra()
        else:
            raise Http404("Comando desconocido")
        # FIXME esto es cutre, lo mejor sería AJAX
        return "../.."


class NodoRemotoComando(OperarioMixin, RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        try:
            nodo = NodoRemoto.objects.get(host_name = self.kwargs['hostname'])
        except:
            raise Http404("Nodo Desconocido")
        try:
            comando = ComandoRemoto.objects.get(comando = self.kwargs['comando'])
        except:
            raise Http404("Comando Desconocido")
        try:
            AMQP_URI = {'AMQP_URI': nodo.url}
            with ClusterRpcProxy(AMQP_URI) as cluster_rpc:
                REMOTO = "{}".format(nodo.host_name)
                eval_str="getattr(cluster_rpc, REMOTO).{}()".format(comando.comando)
                print("Lanzado en nodo {} comando {}".format(REMOTO, comando.comando))
                print(eval(eval_str))
        except Exception as e:
            # TODO: Emitir evento fallo en red expendedor-barrera
            print("ERROR: Communication with node {} failed.".format(nodo.nombre))
            print("   Ignore if it is mode debug.")
            print("   {}".format(e))
        return "../.."

