# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'entity'
        db.create_table('inventory_entity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=1000)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='child', null=True, on_delete=models.SET_NULL, to=orm['inventory.entity'])),
        ))
        db.send_create_signal('inventory', ['entity'])

        # Adding model 'typemachine'
        db.create_table('inventory_typemachine', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('inventory', ['typemachine'])

        # Adding model 'machine'
        db.create_table('inventory_machine', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('serial', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('vendor', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('product', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('entity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.entity'], null=True, on_delete=models.SET_NULL, blank=True)),
            ('packageprofile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deploy.packageprofile'], null=True, on_delete=models.SET_NULL, blank=True)),
            ('lastsave', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('typemachine', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.typemachine'], null=True, on_delete=models.SET_NULL, blank=True)),
            ('netsum', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True)),
            ('ossum', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True)),
            ('softsum', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True)),
        ))
        db.send_create_signal('inventory', ['machine'])

        # Adding M2M table for field packages on 'machine'
        db.create_table('inventory_machine_packages', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('machine', models.ForeignKey(orm['inventory.machine'], null=False)),
            ('package', models.ForeignKey(orm['deploy.package'], null=False))
        ))
        db.create_unique('inventory_machine_packages', ['machine_id', 'package_id'])

        # Adding model 'osdistribution'
        db.create_table('inventory_osdistribution', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('arch', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('systemdrive', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('host', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.machine'])),
        ))
        db.send_create_signal('inventory', ['osdistribution'])

        # Adding model 'net'
        db.create_table('inventory_net', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ip', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('mask', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('mac', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('host', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.machine'])),
        ))
        db.send_create_signal('inventory', ['net'])

        # Adding model 'software'
        db.create_table('inventory_software', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('host', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.machine'])),
        ))
        db.send_create_signal('inventory', ['software'])


    def backwards(self, orm):
        # Deleting model 'entity'
        db.delete_table('inventory_entity')

        # Deleting model 'typemachine'
        db.delete_table('inventory_typemachine')

        # Deleting model 'machine'
        db.delete_table('inventory_machine')

        # Removing M2M table for field packages on 'machine'
        db.delete_table('inventory_machine_packages')

        # Deleting model 'osdistribution'
        db.delete_table('inventory_osdistribution')

        # Deleting model 'net'
        db.delete_table('inventory_net')

        # Deleting model 'software'
        db.delete_table('inventory_software')


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
        'inventory.net': {
            'Meta': {'object_name': 'net'},
            'host': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.machine']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'mac': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'mask': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'inventory.osdistribution': {
            'Meta': {'object_name': 'osdistribution'},
            'arch': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'host': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.machine']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'systemdrive': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'inventory.software': {
            'Meta': {'object_name': 'software'},
            'host': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.machine']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'inventory.typemachine': {
            'Meta': {'object_name': 'typemachine'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['inventory']