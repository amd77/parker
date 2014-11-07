# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Registro.usuario_entrada'
        db.add_column(u'registro_registro', 'usuario_entrada',
                      self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Registro.usuario_salida'
        db.add_column(u'registro_registro', 'usuario_salida',
                      self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Registro.usuario_entrada'
        db.delete_column(u'registro_registro', 'usuario_entrada')

        # Deleting field 'Registro.usuario_salida'
        db.delete_column(u'registro_registro', 'usuario_salida')


    models = {
        u'registro.registro': {
            'Meta': {'ordering': "['-fecha_entrada']", 'object_name': 'Registro'},
            'emitido_ticket': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'euros': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'fecha_entrada': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'fecha_salida': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'matricula': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'minutos': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'usuario_entrada': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'usuario_salida': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['registro']