# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'deployconfig.activate_time_deploy'
        db.add_column('configuration_deployconfig', 'activate_time_deploy',
                      self.gf('django.db.models.fields.CharField')(default='yes', max_length=3),
                      keep_default=False)

        # Adding field 'deployconfig.start_time'
        db.add_column('configuration_deployconfig', 'start_time',
                      self.gf('django.db.models.fields.TimeField')(default=datetime.datetime(2013, 1, 21, 0, 0)),
                      keep_default=False)

        # Adding field 'deployconfig.end_time'
        db.add_column('configuration_deployconfig', 'end_time',
                      self.gf('django.db.models.fields.TimeField')(default=datetime.datetime(2013, 1, 21, 0, 0)),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'deployconfig.activate_time_deploy'
        db.delete_column('configuration_deployconfig', 'activate_time_deploy')

        # Deleting field 'deployconfig.start_time'
        db.delete_column('configuration_deployconfig', 'start_time')

        # Deleting field 'deployconfig.end_time'
        db.delete_column('configuration_deployconfig', 'end_time')


    models = {
        'configuration.deployconfig': {
            'Meta': {'object_name': 'deployconfig'},
            'activate_deploy': ('django.db.models.fields.CharField', [], {'default': "'yes'", 'max_length': '3'}),
            'activate_time_deploy': ('django.db.models.fields.CharField', [], {'default': "'yes'", 'max_length': '3'}),
            'end_time': ('django.db.models.fields.TimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': "'100'"}),
            'start_time': ('django.db.models.fields.TimeField', [], {})
        }
    }

    complete_apps = ['configuration']