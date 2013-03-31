from django.db import models
from django.utils import timezone

import datetime
# Create your models here.
class NewEvent(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    def __unicode__(self):
        return self.name

# Create your models here.
NAME_MAXLEN=50
class User(models.Model):
    name = models.CharField(max_length=NAME_MAXLEN)
    netid = models.CharField(max_length=20)
    friends = models.ForeignKey('self') #recursive relation

class Group(models.Model):
    users = models.ManyToManyField(User)
    name = models.CharField(max_length=NAME_MAXLEN)
    
class Event(models.Model):
    name = models.CharField(max_length=NAME_MAXLEN)
    creator = models.ForeignKey(User)
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    locName = models.CharField(max_length=NAME_MAXLEN)
    locLat = models.FloatField()
    locLong = models.FloatField()
