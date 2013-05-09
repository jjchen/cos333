# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Invite'
        db.create_table(u'frontend_invite', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['frontend.NewEvent'])),
            ('inviter', self.gf('django.db.models.fields.related.ForeignKey')(related_name='inviter', to=orm['frontend.MyUser'])),
            ('invitee', self.gf('django.db.models.fields.related.ForeignKey')(related_name='invitee', to=orm['frontend.MyUser'])),
        ))
        db.send_create_signal(u'frontend', ['Invite'])


    def backwards(self, orm):
        # Deleting model 'Invite'
        db.delete_table(u'frontend_invite')


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
        u'frontend.friends': {
            'Meta': {'object_name': 'Friends'},
            'friends': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'friends'", 'null': 'True', 'to': u"orm['frontend.MyUser']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'name'", 'to': u"orm['frontend.MyUser']"})
        },
        u'frontend.invite': {
            'Meta': {'object_name': 'Invite'},
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['frontend.NewEvent']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invitee': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'invitee'", 'to': u"orm['frontend.MyUser']"}),
            'inviter': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'inviter'", 'to': u"orm['frontend.MyUser']"})
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
            'last_login': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'default': '40.344725'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'default': '-74.6556'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'frontend.newevent': {
            'Meta': {'object_name': 'NewEvent'},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'creator'", 'null': 'True', 'to': u"orm['frontend.MyUser']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'endTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 5, 8, 0, 0)'}),
            'exported': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'groups'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['frontend.MyGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '10', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'default': "'Princeton University'", 'max_length': '200', 'null': 'True'}),
            'lon': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '10', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rsvp': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'rsvp'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['frontend.MyUser']"}),
            'startTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 5, 8, 0, 0)'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['frontend.Tag']", 'symmetrical': 'False'})
        },
        u'frontend.tag': {
            'Meta': {'object_name': 'Tag'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'})
        }
    }

    complete_apps = ['frontend']