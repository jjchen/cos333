# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'NewEvent'
        db.create_table(u'frontend_newevent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('time', self.gf('django.db.models.fields.TimeField')()),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('lat', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=10, blank=True)),
            ('lon', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=10, blank=True)),
        ))
        db.send_create_signal(u'frontend', ['NewEvent'])

        # Adding model 'Building'
        db.create_table(u'frontend_building', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('lat', self.gf('django.db.models.fields.DecimalField')(max_digits=15, decimal_places=10)),
            ('lon', self.gf('django.db.models.fields.DecimalField')(max_digits=15, decimal_places=10)),
        ))
        db.send_create_signal(u'frontend', ['Building'])

        # Adding model 'BuildingAlias'
        db.create_table(u'frontend_buildingalias', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('alias', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('building', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['frontend.Building'])),
        ))
        db.send_create_signal(u'frontend', ['BuildingAlias'])

        # Adding model 'User'
        db.create_table(u'frontend_user', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('netid', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('friends', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['frontend.User'])),
        ))
        db.send_create_signal(u'frontend', ['User'])

        # Adding model 'Group'
        db.create_table(u'frontend_group', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'frontend', ['Group'])

        # Adding M2M table for field users on 'Group'
        db.create_table(u'frontend_group_users', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('group', models.ForeignKey(orm[u'frontend.group'], null=False)),
            ('user', models.ForeignKey(orm[u'frontend.user'], null=False))
        ))
        db.create_unique(u'frontend_group_users', ['group_id', 'user_id'])

        # Adding model 'Event'
        db.create_table(u'frontend_event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['frontend.User'])),
            ('startTime', self.gf('django.db.models.fields.DateTimeField')()),
            ('endTime', self.gf('django.db.models.fields.DateTimeField')()),
            ('locName', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('locLat', self.gf('django.db.models.fields.FloatField')()),
            ('locLong', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'frontend', ['Event'])


    def backwards(self, orm):
        # Deleting model 'NewEvent'
        db.delete_table(u'frontend_newevent')

        # Deleting model 'Building'
        db.delete_table(u'frontend_building')

        # Deleting model 'BuildingAlias'
        db.delete_table(u'frontend_buildingalias')

        # Deleting model 'User'
        db.delete_table(u'frontend_user')

        # Deleting model 'Group'
        db.delete_table(u'frontend_group')

        # Removing M2M table for field users on 'Group'
        db.delete_table('frontend_group_users')

        # Deleting model 'Event'
        db.delete_table(u'frontend_event')


    models = {
        u'frontend.building': {
            'Meta': {'object_name': 'Building'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'max_digits': '15', 'decimal_places': '10'}),
            'lon': ('django.db.models.fields.DecimalField', [], {'max_digits': '15', 'decimal_places': '10'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'frontend.buildingalias': {
            'Meta': {'object_name': 'BuildingAlias'},
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'building': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['frontend.Building']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'frontend.event': {
            'Meta': {'object_name': 'Event'},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['frontend.User']"}),
            'endTime': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locLat': ('django.db.models.fields.FloatField', [], {}),
            'locLong': ('django.db.models.fields.FloatField', [], {}),
            'locName': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'startTime': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'frontend.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['frontend.User']", 'symmetrical': 'False'})
        },
        u'frontend.newevent': {
            'Meta': {'object_name': 'NewEvent'},
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '10', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'lon': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '10', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'time': ('django.db.models.fields.TimeField', [], {})
        },
        u'frontend.user': {
            'Meta': {'object_name': 'User'},
            'friends': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['frontend.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'netid': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        }
    }

    complete_apps = ['frontend']