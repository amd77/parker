"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from registro.models import get_tarifa

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(get_tarifa(0), 0.0)
        self.assertEqual(get_tarifa(4), 0.0)
        self.assertEqual(get_tarifa(5), 0.0)
        self.assertEqual(get_tarifa(5.1), 0.5)
        self.assertEqual(get_tarifa(29.9), 0.5)
        self.assertEqual(get_tarifa(30.0), 0.5)
        self.assertEqual(get_tarifa(30.1), 0.9)
        self.assertEqual(get_tarifa(599), 4.8)
        self.assertEqual(get_tarifa(601), 4.8)

