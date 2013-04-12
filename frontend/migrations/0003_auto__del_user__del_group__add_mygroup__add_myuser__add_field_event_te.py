# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'User'
        db.delete_table(u'frontend_user')

        # Deleting model 'Group'
        db.delete_table(u'frontend_group')

        # Removing M2M table for field users on 'Group'
        db.delete_table('frontend_group_users')

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

        # Adding model 'MyUser'
        db.create_table(u'frontend_myuser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('user_id', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'frontend', ['MyUser'])

        # Adding field 'Event.testField'
        db.add_column(u'frontend_event', 'testField',
                      self.gf('django.db.models.fields.CharField')(default='ihavenoideawhatiamdoing', max_length=40),
                      keep_default=False)


        # Changing field 'Event.creator'
        db.alter_column(u'frontend_event', 'creator_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['frontend.MyUser']))

        # Changing field 'NewEvent.tags'
        db.alter_column(u'frontend_newevent', 'tags', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

    def backwards(self, orm):
        # Adding model 'User'
        db.create_table(u'frontend_user', (
            ('friends', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['frontend.User'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('netid', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
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

        # Deleting model 'MyGroup'
        db.delete_table(u'frontend_mygroup')

        # Removing M2M table for field users on 'MyGroup'
        db.delete_table('frontend_mygroup_users')

        # Deleting model 'MyUser'
        db.delete_table(u'frontend_myuser')

        # Deleting field 'Event.testField'
        db.delete_column(u'frontend_event', 'testField')


        # Changing field 'Event.creator'
        db.alter_column(u'frontend_event', 'creator_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['frontend.User']))

        # Changing field 'NewEvent.tags'
        db.alter_column(u'frontend_newevent', 'tags', self.gf('django.db.models.fields.CharField')(default='all', max_length=200))

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
            'testField': ('django.db.models.fields.CharField', [], {'default': "'ihavenoideawhatiamdoing'", 'max_length': '40'})
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