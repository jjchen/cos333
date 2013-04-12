# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Event.testField2'
        db.add_column(u'frontend_event', 'testField2',
                      self.gf('django.db.models.fields.CharField')(default='ihavenoideawhatamdoing', max_length=40),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Event.testField2'
        db.delete_column(u'frontend_event', 'testField2')


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
            'testField': ('django.db.models.fields.CharField', [], {'default': "'ihavenoideawhatiamdoing'", 'max_length': '40'}),
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