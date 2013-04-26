# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Friends'
        db.create_table(u'frontend_friends', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.related.ForeignKey')(related_name='name', to=orm['frontend.MyUser'])),
        ))
        db.send_create_signal(u'frontend', ['Friends'])

        # Adding M2M table for field friends on 'Friends'
        db.create_table(u'frontend_friends_friends', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('friends', models.ForeignKey(orm[u'frontend.friends'], null=False)),
            ('myuser', models.ForeignKey(orm[u'frontend.myuser'], null=False))
        ))
        db.create_unique(u'frontend_friends_friends', ['friends_id', 'myuser_id'])

        # Adding field 'NewEvent.creator'
        db.add_column(u'frontend_newevent', 'creator',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='creator', null=True, to=orm['frontend.MyUser']),
                      keep_default=False)

        # Adding M2M table for field groups on 'NewEvent'
        db.create_table(u'frontend_newevent_groups', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('newevent', models.ForeignKey(orm[u'frontend.newevent'], null=False)),
            ('mygroup', models.ForeignKey(orm[u'frontend.mygroup'], null=False))
        ))
        db.create_unique(u'frontend_newevent_groups', ['newevent_id', 'mygroup_id'])

        # Adding M2M table for field rsvp on 'NewEvent'
        db.create_table(u'frontend_newevent_rsvp', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('newevent', models.ForeignKey(orm[u'frontend.newevent'], null=False)),
            ('myuser', models.ForeignKey(orm[u'frontend.myuser'], null=False))
        ))
        db.create_unique(u'frontend_newevent_rsvp', ['newevent_id', 'myuser_id'])


    def backwards(self, orm):
        # Deleting model 'Friends'
        db.delete_table(u'frontend_friends')

        # Removing M2M table for field friends on 'Friends'
        db.delete_table('frontend_friends_friends')

        # Deleting field 'NewEvent.creator'
        db.delete_column(u'frontend_newevent', 'creator_id')

        # Removing M2M table for field groups on 'NewEvent'
        db.delete_table('frontend_newevent_groups')

        # Removing M2M table for field rsvp on 'NewEvent'
        db.delete_table('frontend_newevent_rsvp')


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
        u'frontend.calevent': {
            'Meta': {'object_name': 'CalEvent'},
            'details': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '30'})
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
            'testField2': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'frontend.friends': {
            'Meta': {'object_name': 'Friends'},
            'friends': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'friends'", 'null': 'True', 'to': u"orm['frontend.MyUser']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'name'", 'to': u"orm['frontend.MyUser']"})
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
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'creator'", 'null': 'True', 'to': u"orm['frontend.MyUser']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'groups'", 'null': 'True', 'to': u"orm['frontend.MyGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '10', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'lon': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '10', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'rsvp': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'rsvp'", 'null': 'True', 'to': u"orm['frontend.MyUser']"}),
            'tags': ('django.db.models.fields.CharField', [], {'default': "'all'", 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'time': ('django.db.models.fields.TimeField', [], {})
        }
    }

    complete_apps = ['frontend']