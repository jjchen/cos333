# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tag'
        db.create_table(u'frontend_tag', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50, primary_key=True)),
        ))
        db.send_create_signal(u'frontend', ['Tag'])

        # Adding model 'MyUser'
        db.create_table(u'frontend_myuser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('user_id', self.gf('django.db.models.fields.CharField')(max_length=50)),
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

        # Adding model 'NewEvent'
        db.create_table(u'frontend_newevent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('startTime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 5, 7, 0, 0))),
            ('endTime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 5, 7, 0, 0))),
            ('location', self.gf('django.db.models.fields.CharField')(default='Princeton University', max_length=200, null=True)),
            ('private', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('lat', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=10, blank=True)),
            ('lon', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=10, blank=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='creator', null=True, to=orm['frontend.MyUser'])),
        ))
        db.send_create_signal(u'frontend', ['NewEvent'])

        # Adding M2M table for field tags on 'NewEvent'
        db.create_table(u'frontend_newevent_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('newevent', models.ForeignKey(orm[u'frontend.newevent'], null=False)),
            ('tag', models.ForeignKey(orm[u'frontend.tag'], null=False))
        ))
        db.create_unique(u'frontend_newevent_tags', ['newevent_id', 'tag_id'])

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

        # Adding model 'CalEvent'
        db.create_table(u'frontend_calevent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('details', self.gf('django.db.models.fields.CharField')(max_length=250)),
        ))
        db.send_create_signal(u'frontend', ['CalEvent'])


    def backwards(self, orm):
        # Deleting model 'Tag'
        db.delete_table(u'frontend_tag')

        # Deleting model 'MyUser'
        db.delete_table(u'frontend_myuser')

        # Deleting model 'MyGroup'
        db.delete_table(u'frontend_mygroup')

        # Removing M2M table for field users on 'MyGroup'
        db.delete_table('frontend_mygroup_users')

        # Deleting model 'NewEvent'
        db.delete_table(u'frontend_newevent')

        # Removing M2M table for field tags on 'NewEvent'
        db.delete_table('frontend_newevent_tags')

        # Removing M2M table for field groups on 'NewEvent'
        db.delete_table('frontend_newevent_groups')

        # Removing M2M table for field rsvp on 'NewEvent'
        db.delete_table('frontend_newevent_rsvp')

        # Deleting model 'Building'
        db.delete_table(u'frontend_building')

        # Deleting model 'BuildingAlias'
        db.delete_table(u'frontend_buildingalias')

        # Deleting model 'Friends'
        db.delete_table(u'frontend_friends')

        # Removing M2M table for field friends on 'Friends'
        db.delete_table('frontend_friends_friends')

        # Deleting model 'CalEvent'
        db.delete_table(u'frontend_calevent')


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
            'user_id': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'frontend.newevent': {
            'Meta': {'object_name': 'NewEvent'},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'creator'", 'null': 'True', 'to': u"orm['frontend.MyUser']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'endTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 5, 7, 0, 0)'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'groups'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['frontend.MyGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '10', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'default': "'Princeton University'", 'max_length': '200', 'null': 'True'}),
            'lon': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '10', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rsvp': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'rsvp'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['frontend.MyUser']"}),
            'startTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 5, 7, 0, 0)'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['frontend.Tag']", 'symmetrical': 'False'})
        },
        u'frontend.tag': {
            'Meta': {'object_name': 'Tag'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'})
        }
    }

    complete_apps = ['frontend']