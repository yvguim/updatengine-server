# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'deployconfig.name'
        db.add_column('configuration_deployconfig', 'name',
                      self.gf('django.db.models.fields.CharField')(default='Default configuration', max_length='100'),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'deployconfig.name'
        db.delete_column('configuration_deployconfig', 'name')


    models = {
        'configuration.deployconfig': {
            'Meta': {'object_name': 'deployconfig'},
            'activate_deploy': ('django.db.models.fields.CharField', [], {'default': "'yes'", 'max_length': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': "'100'"})
        }
    }

    complete_apps = ['configuration']