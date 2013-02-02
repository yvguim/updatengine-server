# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'packagecondition'
        db.create_table('deploy_packagecondition', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('depends', self.gf('django.db.models.fields.CharField')(default='installed', max_length=12)),
            ('softwarename', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('softwareversion', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal('deploy', ['packagecondition'])

        # Adding model 'package'
        db.create_table('deploy_package', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('command', self.gf('django.db.models.fields.TextField')(max_length=1000)),
            ('packagesum', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True)),
            ('filename', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('deploy', ['package'])

        # Adding M2M table for field conditions on 'package'
        db.create_table('deploy_package_conditions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('package', models.ForeignKey(orm['deploy.package'], null=False)),
            ('packagecondition', models.ForeignKey(orm['deploy.packagecondition'], null=False))
        ))
        db.create_unique('deploy_package_conditions', ['package_id', 'packagecondition_id'])

        # Adding model 'packagehistory'
        db.create_table('deploy_packagehistory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('command', self.gf('django.db.models.fields.TextField')(max_length=1000, null=True, blank=True)),
            ('packagesum', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True)),
            ('filename', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('machine', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.machine'])),
            ('package', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deploy.package'], null=True, on_delete=models.SET_NULL, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='Programmed', max_length=100, null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('deploy', ['packagehistory'])

        # Adding model 'packageprofile'
        db.create_table('deploy_packageprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
        ))
        db.send_create_signal('deploy', ['packageprofile'])

        # Adding M2M table for field packages on 'packageprofile'
        db.create_table('deploy_packageprofile_packages', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('packageprofile', models.ForeignKey(orm['deploy.packageprofile'], null=False)),
            ('package', models.ForeignKey(orm['deploy.package'], null=False))
        ))
        db.create_unique('deploy_packageprofile_packages', ['packageprofile_id', 'package_id'])


    def backwards(self, orm):
        # Deleting model 'packagecondition'
        db.delete_table('deploy_packagecondition')

        # Deleting model 'package'
        db.delete_table('deploy_package')

        # Removing M2M table for field conditions on 'package'
        db.delete_table('deploy_package_conditions')

        # Deleting model 'packagehistory'
        db.delete_table('deploy_packagehistory')

        # Deleting model 'packageprofile'
        db.delete_table('deploy_packageprofile')

        # Removing M2M table for field packages on 'packageprofile'
        db.delete_table('deploy_packageprofile_packages')


    models = {
        'deploy.package': {
            'Meta': {'object_name': 'package'},
            'command': ('django.db.models.fields.TextField', [], {'max_length': '1000'}),
            'conditions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['deploy.packagecondition']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'filename': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'packagesum': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'})
        },
        'deploy.packagecondition': {
            'Meta': {'object_name': 'packagecondition'},
            'depends': ('django.db.models.fields.CharField', [], {'default': "'installed'", 'max_length': '12'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'softwarename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'softwareversion': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'deploy.packagehistory': {
            'Meta': {'object_name': 'packagehistory'},
            'command': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'machine': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.machine']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['deploy.package']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'packagesum': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'Programmed'", 'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'deploy.packageprofile': {
            'Meta': {'object_name': 'packageprofile'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'packages': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['deploy.package']", 'null': 'True', 'blank': 'True'})
        },
        'inventory.entity': {
            'Meta': {'object_name': 'entity'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '1000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'child'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['inventory.entity']"})
        },
        'inventory.machine': {
            'Meta': {'object_name': 'machine'},
            'entity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.entity']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastsave': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'netsum': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'ossum': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'packageprofile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['deploy.packageprofile']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'packages': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['deploy.package']", 'null': 'True', 'blank': 'True'}),
            'product': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'serial': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'softsum': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'typemachine': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.typemachine']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'vendor': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'inventory.typemachine': {
            'Meta': {'object_name': 'typemachine'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['deploy']