# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'deployconfig'
        db.create_table('configuration_deployconfig', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('activate_deploy', self.gf('django.db.models.fields.CharField')(default='yes', max_length=3)),
        ))
        db.send_create_signal('configuration', ['deployconfig'])


    def backwards(self, orm):
        # Deleting model 'deployconfig'
        db.delete_table('configuration_deployconfig')


    models = {
        'configuration.deployconfig': {
            'Meta': {'object_name': 'deployconfig'},
            'activate_deploy': ('django.db.models.fields.CharField', [], {'default': "'yes'", 'max_length': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['configuration']