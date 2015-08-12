# -*- coding: utf-8 -*-

from django.template import Library
register = Library()


@register.assignment_tag
def multicol(vector, count):
    # redondear hacia arriba (p.ej; 30+3-1/3=10, 31+3-1/3=11)
    vector = list(vector)
    dn = (len(vector) + count - 1) / count
    return [vector[i*dn:(i+1)*dn] for i in range(count)]
