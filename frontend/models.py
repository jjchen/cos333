from django.db import models
from django.utils import timezone
from django.forms import ModelForm

import datetime
# Create your models here.
class NewEvent(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    lat = models.DecimalField(max_digits=15, decimal_places=10, blank=True, null=True)
    lon = models.DecimalField(max_digits=15, decimal_places=10, blank=True, null=True)
    tags = models.CharField(max_length=200, blank = True, null=True)
    def __unicode__(self):
        return self.name

class NewEventForm(ModelForm):
    class Meta:
        model = NewEvent

class Building(models.Model):
    name = models.CharField(max_length=200)
    lat = models.DecimalField(max_digits=15, decimal_places=10)
    lon = models.DecimalField(max_digits=15, decimal_places=10)

class BuildingAlias(models.Model):
    alias = models.CharField(max_length=200)
    building = models.ForeignKey(Building)

# Create your models here.
NAME_MAXLEN=50
class MyUser(models.Model):
    first_name = models.CharField(max_length=NAME_MAXLEN)
    last_name = models.CharField(max_length=NAME_MAXLEN)
    user_id = models.CharField(max_length=20)
	# friends = models.ForeignKey('self', null=True) #recursive relation

class MyGroup(models.Model):
	users = models.ManyToManyField(MyUser, related_name="users")
	#creator = models.ForeignKey(MyUser, related_name="creator")
	creator = models.CharField(max_length=NAME_MAXLEN)
	name = models.CharField(max_length=NAME_MAXLEN)

    
class Event(models.Model):
    name = models.CharField(max_length=NAME_MAXLEN)
    creator = models.ForeignKey(MyUser)
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    locName = models.CharField(max_length=NAME_MAXLEN)
    locLat = models.FloatField()
    locLong = models.FloatField()
