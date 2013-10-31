# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'packageprofile', fields ['name']
        db.delete_unique(u'deploy_packageprofile', ['name'])

        # Removing unique constraint on 'timeprofile', fields ['name']
        db.delete_unique(u'deploy_timeprofile', ['name'])


    def backwards(self, orm):
        # Adding unique constraint on 'timeprofile', fields ['name']
        db.create_unique(u'deploy_timeprofile', ['name'])

        # Adding unique constraint on 'packageprofile', fields ['name']
        db.create_unique(u'deploy_packageprofile', ['name'])


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'deploy.impex': {
            'Meta': {'ordering': "['name']", 'object_name': 'impex'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '500'}),
            'filename': ('django.db.models.fields.files.FileField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['deploy.package']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'packagesum': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'})
        },
        u'deploy.package': {
            'Meta': {'ordering': "['name']", 'object_name': 'package'},
            'command': ('django.db.models.fields.TextField', [], {'max_length': '1000'}),
            'conditions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['deploy.packagecondition']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'}),
            'entity': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['inventory.entity']", 'null': 'True', 'blank': 'True'}),
            'exclusive_editor': ('django.db.models.fields.CharField', [], {'default': "'no'", 'max_length': '3'}),
            'filename': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ignoreperiod': ('django.db.models.fields.CharField', [], {'default': "'no'", 'max_length': '3'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'packagesum': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'public': ('django.db.models.fields.CharField', [], {'default': "'no'", 'max_length': '3'})
        },
        u'deploy.packagecondition': {
            'Meta': {'ordering': "['name']", 'object_name': 'packagecondition'},
            'depends': ('django.db.models.fields.CharField', [], {'default': "'installed'", 'max_length': '12'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'}),
            'entity': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['inventory.entity']", 'null': 'True', 'blank': 'True'}),
            'exclusive_editor': ('django.db.models.fields.CharField', [], {'default': "'no'", 'max_length': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'softwarename': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'softwareversion': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '500', 'null': 'True', 'blank': 'True'})
        },
        u'deploy.packagehistory': {
            'Meta': {'ordering': "['date']", 'object_name': 'packagehistory'},
            'command': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'machine': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.machine']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deploy.package']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'packagesum': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'Programmed'", 'max_length': '500', 'null': 'True', 'blank': 'True'})
        },
        u'deploy.packageprofile': {
            'Meta': {'ordering': "['name']", 'object_name': 'packageprofile'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'}),
            'entity': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'package_profile_entity'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['inventory.entity']"}),
            'exclusive_editor': ('django.db.models.fields.CharField', [], {'default': "'no'", 'max_length': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'packages': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['deploy.package']", 'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'child'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['deploy.packageprofile']"})
        },
        u'deploy.packagewakeonlan': {
            'Meta': {'ordering': "['date']", 'object_name': 'packagewakeonlan'},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'machines': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['inventory.machine']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'Programmed'", 'max_length': '100'})
        },
        u'deploy.timeprofile': {
            'Meta': {'ordering': "['start_time']", 'object_name': 'timeprofile'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'}),
            'end_time': ('django.db.models.fields.TimeField', [], {}),
            'entity': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'time_profile_entity'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['inventory.entity']"}),
            'exclusive_editor': ('django.db.models.fields.CharField', [], {'default': "'no'", 'max_length': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'start_time': ('django.db.models.fields.TimeField', [], {})
        },
        u'inventory.entity': {
            'Meta': {'ordering': "['name']", 'object_name': 'entity'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '1000'}),
            'force_packageprofile': ('django.db.models.fields.CharField', [], {'default': "'no'", 'max_length': '3'}),
            'force_timeprofile': ('django.db.models.fields.CharField', [], {'default': "'no'", 'max_length': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'old_packageprofile': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'old_packageprofile'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['deploy.packageprofile']"}),
            'old_timeprofile': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'old_timeprofile'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['deploy.timeprofile']"}),
            'packageprofile': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'pprofile'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['deploy.packageprofile']"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'child'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['inventory.entity']"}),
            'timeprofile': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'timeprofile'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['deploy.timeprofile']"})
        },
        u'inventory.machine': {
            'Meta': {'object_name': 'machine'},
            'domain': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'entity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.entity']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'lastsave': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'manualy_created': ('django.db.models.fields.CharField', [], {'default': "'yes'", 'max_length': '3'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'netsum': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'ossum': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'packageprofile': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deploy.packageprofile']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'packages': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['deploy.package']", 'null': 'True', 'blank': 'True'}),
            'product': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'serial': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'softsum': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'timeprofile': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deploy.timeprofile']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'typemachine': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.typemachine']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'vendor': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'inventory.typemachine': {
            'Meta': {'object_name': 'typemachine'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['deploy']