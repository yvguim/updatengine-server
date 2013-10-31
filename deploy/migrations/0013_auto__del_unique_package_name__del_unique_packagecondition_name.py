# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'packagecondition', fields ['name']
        db.delete_unique(u'deploy_packagecondition', ['name'])

        # Removing unique constraint on 'package', fields ['name']
        db.delete_unique(u'deploy_package', ['name'])

        # Adding M2M table for field entity on 'package'
        m2m_table_name = db.shorten_name(u'deploy_package_entity')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('package', models.ForeignKey(orm[u'deploy.package'], null=False)),
            ('entity', models.ForeignKey(orm[u'inventory.entity'], null=False))
        ))
        db.create_unique(m2m_table_name, ['package_id', 'entity_id'])

        # Adding M2M table for field entity on 'packagecondition'
        m2m_table_name = db.shorten_name(u'deploy_packagecondition_entity')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('packagecondition', models.ForeignKey(orm[u'deploy.packagecondition'], null=False)),
            ('entity', models.ForeignKey(orm[u'inventory.entity'], null=False))
        ))
        db.create_unique(m2m_table_name, ['packagecondition_id', 'entity_id'])


    def backwards(self, orm):
        # Removing M2M table for field entity on 'package'
        db.delete_table(db.shorten_name(u'deploy_package_entity'))

        # Adding unique constraint on 'package', fields ['name']
        db.create_unique(u'deploy_package', ['name'])

        # Removing M2M table for field entity on 'packagecondition'
        db.delete_table(db.shorten_name(u'deploy_packagecondition_entity'))

        # Adding unique constraint on 'packagecondition', fields ['name']
        db.create_unique(u'deploy_packagecondition', ['name'])


    models = {
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
            'entity': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['inventory.entity']", 'null': 'True', 'blank': 'True'}),
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
            'entity': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['inventory.entity']", 'null': 'True', 'blank': 'True'}),
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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
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
            'end_time': ('django.db.models.fields.TimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
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
            'packageprofile': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deploy.packageprofile']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'child'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['inventory.entity']"}),
            'timeprofile': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deploy.timeprofile']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'})
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