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
            ('tags', self.gf('django.db.models.fields.CharField')(default='all', max_length=200, null=True, blank=True)),
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

        # Adding model 'MyUser'
        db.create_table(u'frontend_myuser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('user_id', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('latitude', self.gf('django.db.models.fields.FloatField')(default=40.344725)),
            ('longitude', self.gf('django.db.models.fields.FloatField')(default=-74.6556)),
        ))
        db.send_create_signal(u'frontend', ['MyUser'])

        # Adding model 'MyGroup'
        db.create_table(u'frontend_mygroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creator', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'frontend', ['MyGroup'])

        # Adding M2M table for field users on 'MyGroup'
        db.create_table(u'frontend_mygroup_users', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('mygroup', models.ForeignKey(orm[u'frontend.mygroup'], null=False)),
            ('myuser', models.ForeignKey(orm[u'frontend.myuser'], null=False))
        ))
        db.create_unique(u'frontend_mygroup_users', ['mygroup_id', 'myuser_id'])

        # Adding model 'Event'
        db.create_table(u'frontend_event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('testField2', self.gf('django.db.models.fields.CharField')(default='ihavenoideawhatamdoing', max_length=40)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['frontend.MyUser'])),
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

        # Deleting model 'MyUser'
        db.delete_table(u'frontend_myuser')

        # Deleting model 'MyGroup'
        db.delete_table(u'frontend_mygroup')

        # Removing M2M table for field users on 'MyGroup'
        db.delete_table('frontend_mygroup_users')

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
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['frontend.MyUser']"}),
            'endTime': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locLat': ('django.db.models.fields.FloatField', [], {}),
            'locLong': ('django.db.models.fields.FloatField', [], {}),
            'locName': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'startTime': ('django.db.models.fields.DateTimeField', [], {}),
            'testField2': ('django.db.models.fields.CharField', [], {'default': "'ihavenoideawhatamdoing'", 'max_length': '40'})
        },
        u'frontend.mygroup': {
            'Meta': {'object_name': 'MyGroup'},
            'creator': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'users'", 'symmetrical': 'False', 'to': u"orm['frontend.MyUser']"})
        },
        u'frontend.myuser': {
            'Meta': {'object_name': 'MyUser'},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'default': '40.344725'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'default': '-74.6556'}),
            'user_id': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'frontend.newevent': {
            'Meta': {'object_name': 'NewEvent'},
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '10', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'lon': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '10', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'tags': ('django.db.models.fields.CharField', [], {'default': "'all'", 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'time': ('django.db.models.fields.TimeField', [], {})
        }
    }

    complete_apps = ['frontend']