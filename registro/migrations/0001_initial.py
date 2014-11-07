# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Registro'
        db.create_table(u'registro_registro', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('matricula', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('fecha_entrada', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('fecha_salida', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('minutos', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('euros', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('emitido_ticket', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'registro', ['Registro'])


    def backwards(self, orm):
        # Deleting model 'Registro'
        db.delete_table(u'registro_registro')


    models = {
        u'registro.registro': {
            'Meta': {'ordering': "['-fecha_entrada']", 'object_name': 'Registro'},
            'emitido_ticket': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'euros': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'fecha_entrada': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'fecha_salida': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'matricula': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'minutos': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['registro']