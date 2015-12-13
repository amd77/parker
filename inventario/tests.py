from django.test import TestCase
from django.contrib.auth.models import User
from empresa.models import Empresa, Operario
from inventario.models import Parking, Tarifa
import datetime


class Base(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username="john")
        cls.user.set_password("smith")
        cls.user.save()
        cls.empresa = Empresa.objects.create(nombre="Empresa")
        cls.parking = Parking.objects.create(nombre="Parking", empresa=cls.empresa, plazas=100)
        cls.operario = Operario.objects.create(user=cls.user, empresa=cls.empresa)

TARIFAS = [
    # Esta formula es:
    #  precio = 0                            para -5 hora
    #  precio = 0.50                         para 5-30 hora
    #  precio = 0.491 + hora / 60 * 0.515 para 30 hora-6 horas
    #  precio = 4.80                         para 6-10 horas
    #  precio = 6.00                         para +10 horas
    ("00:00:00", 0.00),
    ("00:05:00", 0.50),
    ("00:31:00", 0.60),
    ("00:41:00", 0.80),
    ("00:51:00", 0.90),
    ("01:01:00", 1.00),
    ("01:11:00", 1.10),
    ("01:21:00", 1.20),
    ("01:31:00", 1.30),
    ("01:41:00", 1.40),
    ("01:51:00", 1.50),
    ("02:01:00", 1.60),
    ("02:11:00", 1.65),
    ("02:21:00", 1.70),
    ("02:31:00", 1.80),
    ("02:41:00", 1.90),
    ("02:51:00", 2.00),
    ("03:01:00", 2.10),
    ("03:11:00", 2.15),
    ("03:21:00", 2.20),
    ("03:31:00", 2.30),
    ("03:41:00", 2.40),
    ("03:51:00", 2.50),
    ("04:01:00", 2.60),
    ("04:11:00", 2.65),
    ("04:21:00", 2.70),
    ("04:31:00", 2.80),
    ("04:41:00", 2.90),
    ("04:51:00", 3.00),
    ("05:01:00", 3.10),
    ("05:11:00", 3.15),
    ("05:21:00", 3.20),
    ("05:31:00", 3.30),
    ("05:41:00", 3.40),
    ("05:51:00", 3.50),
    ("06:01:00", 4.80),
    ("10:00:00", 6.00),
]


def hhmmss_to_timedelta(hhmmss):
    f1 = datetime.datetime.strptime(hhmmss, "%H:%M:%S")
    f2 = datetime.datetime(1900, 1, 1)
    return f1-f2


def crea_tarifas(parking):
    parking.tarifa_set.all().delete()
    for hora, precio in TARIFAS:
        Tarifa.objects.create(parking=parking, hora=hhmmss_to_timedelta(hora), precio=precio)


def _minutos(hhmmss):
    f1 = datetime.datetime.strptime(hhmmss, "%H:%M:%S")
    f2 = datetime.datetime(1900, 1, 1)
    return (f1-f2).total_seconds()/60


class TestLogin(Base):
    def test_raiz_falla(self):
        client = self.client_class()
        response = client.get("/")
        self.assertEqual(response.status_code, 404)

    def test_client_no_login(self):
        client = self.client_class()
        response = client.get("/parker/")
        self.assertEqual(response.status_code, 302)

    def test_client_logged_in(self):
        client = self.client_class()
        response = client.post('/parker/accounts/login/', {'username': 'john', 'password': 'smith'})
        self.assertRedirects(response, "/parker/")
        response = client.get("/parker/")
        self.assertContains(response, "0 coches dentro")
        self.assertContains(response, "Pase el carnet de abonado o el ticket")


class TestTarifas(Base):
    def setUp(self):
        self.client.post('/parker/accounts/login/', {'username': 'john', 'password': 'smith'})

    @classmethod
    def setUpTestData(cls):
        super(TestTarifas, cls).setUpTestData()
        crea_tarifas(cls.parking)

    def test_render_pagina(self):
        response = self.client.get("/parker/tarifas")
        self.assertContains(response, "0:04")

    def test_tarifario(self):
        for hhmmss, euros in TARIFAS:
            self.assertEqual(self.parking.get_tarifa(_minutos(hhmmss)), euros)

    def test_minutos(self):
        self.assertEqual(self.parking.get_tarifa(50), 0.8)
        self.assertEqual(self.parking.get_tarifa(51), 0.9)

    def test_get_dia(self):
        self.assertEqual(self.parking.get_dia(), 6.0)

    def test_casi_un_dia(self):
        self.assertEqual(self.parking.get_tarifa(24*60-1), 6.0)

    def test_un_dia(self):
        self.assertEqual(self.parking.get_tarifa(24*60), 6.0)

    def test_dos_dias_y_pico(self):
        self.assertEqual(self.parking.get_tarifa(2*24*60+10), 2*6.0+0.5)
