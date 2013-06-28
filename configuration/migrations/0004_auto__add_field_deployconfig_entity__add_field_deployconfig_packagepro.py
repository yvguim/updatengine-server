# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'deployconfig.entity'
        db.add_column('configuration_deployconfig', 'entity',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['inventory.entity'], null=True, on_delete=models.SET_NULL, blank=True),
                      keep_default=False)

        # Adding field 'deployconfig.packageprofile'
        db.add_column('configuration_deployconfig', 'packageprofile',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['deploy.packageprofile'], null=True, on_delete=models.SET_NULL, blank=True),
                      keep_default=False)

        # Adding field 'deployconfig.timeprofile'
        db.add_column('configuration_deployconfig', 'timeprofile',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['deploy.timeprofile'], null=True, on_delete=models.SET_NULL, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'deployconfig.entity'
        db.delete_column('configuration_deployconfig', 'entity_id')

        # Deleting field 'deployconfig.packageprofile'
        db.delete_column('configuration_deployconfig', 'packageprofile_id')

        # Deleting field 'deployconfig.timeprofile'
        db.delete_column('configuration_deployconfig', 'timeprofile_id')


    models = {
        'configuration.deployconfig': {
            'Meta': {'object_name': 'deployconfig'},
            'activate_deploy': ('django.db.models.fields.CharField', [], {'default': "'yes'", 'max_length': '3'}),
            'activate_time_deploy': ('django.db.models.fields.CharField', [], {'default': "'no'", 'max_length': '3'}),
            'end_time': ('django.db.models.fields.TimeField', [], {}),
            'entity': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['inventory.entity']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': "'100'"}),
            'packageprofile': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['deploy.packageprofile']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'start_time': ('django.db.models.fields.TimeField', [], {}),
            'timeprofile': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['deploy.timeprofile']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'})
        },
        'deploy.package': {
            'Meta': {'object_name': 'package'},
            'command': ('django.db.models.fields.TextField', [], {'max_length': '1000'}),
            'conditions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['deploy.packagecondition']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'filename': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ignoreperiod': ('django.db.models.fields.CharField', [], {'default': "'no'", 'max_length': '3'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'packagesum': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'public': ('django.db.models.fields.CharField', [], {'default': "'no'", 'max_length': '3'})
        },
        'deploy.packagecondition': {
            'Meta': {'object_name': 'packagecondition'},
            'depends': ('django.db.models.fields.CharField', [], {'default': "'installed'", 'max_length': '12'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'softwarename': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'softwareversion': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '500', 'null': 'True', 'blank': 'True'})
        },
        'deploy.packageprofile': {
            'Meta': {'object_name': 'packageprofile'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'packages': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['deploy.package']", 'null': 'True', 'blank': 'True'})
        },
        'deploy.timeprofile': {
            'Meta': {'object_name': 'timeprofile'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'end_time': ('django.db.models.fields.TimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'start_time': ('django.db.models.fields.TimeField', [], {})
        },
        'inventory.entity': {
            'Meta': {'object_name': 'entity'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '1000'}),
            'force_packageprofile': ('django.db.models.fields.CharField', [], {'default': "'no'", 'max_length': '3'}),
            'force_timeprofile': ('django.db.models.fields.CharField', [], {'default': "'no'", 'max_length': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'old_packageprofile': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'old_packageprofile'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['deploy.packageprofile']"}),
            'old_timeprofile': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'old_timeprofile'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['deploy.timeprofile']"}),
            'packageprofile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['deploy.packageprofile']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'child'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['inventory.entity']"}),
            'timeprofile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['deploy.timeprofile']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'})
        }
    }

    complete_apps = ['configuration']