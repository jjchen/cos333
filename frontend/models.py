import datetime

from django.db import models
from django.utils import timezone
from django.forms import ModelForm

NAME_MAXLEN=50

class MyUser(models.Model):
    first_name = models.CharField(max_length=NAME_MAXLEN)
    last_name = models.CharField(max_length=NAME_MAXLEN)
    user_id = models.CharField(max_length=20)
    latitude = models.FloatField(default=40.344725)
    longitude = models.FloatField(default=-74.6556)
    # friends = models.ForeignKey('self', null=True) #recursive relation

class MyGroup(models.Model):
    users = models.ManyToManyField(MyUser, related_name="users")
    #creator = models.ForeignKey(MyUser, related_name="creator")
    creator = models.CharField(max_length=NAME_MAXLEN)
    name = models.CharField(max_length=NAME_MAXLEN)

# Create your models here.
class NewEvent(models.Model):
    name = models.CharField(max_length=200)
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    location = models.CharField(max_length=200)
    private = models.BooleanField(default=False)
    lat = models.DecimalField(max_digits=15, decimal_places=10, blank=True, null=True)
    lon = models.DecimalField(max_digits=15, decimal_places=10, blank=True, null=True)
    tags = models.CharField(max_length=200, blank = True, null=True, default="all")
    creator = models.ForeignKey(MyUser, related_name="creator", blank=True, null=True)
    groups = models.ManyToManyField(MyGroup, related_name="groups", blank=True, null=True)
    rsvp = models.ManyToManyField(MyUser, related_name="rsvp", blank=True, null=True)

    def __unicode__(self):
        return self.name

class Building(models.Model):
    name = models.CharField(max_length=200)
    lat = models.DecimalField(max_digits=15, decimal_places=10)
    lon = models.DecimalField(max_digits=15, decimal_places=10)

class BuildingAlias(models.Model):
    alias = models.CharField(max_length=200)
    building = models.ForeignKey(Building)

class Friends(models.Model):
    name = models.ForeignKey(MyUser, related_name="name")
    friends = models.ManyToManyField(MyUser, related_name="friends", null=True)

class CalEvent(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    text = models.CharField(max_length=30)
    details = models.CharField(max_length=250)
