import datetime

from django.db import models
from django.utils import timezone
from django.forms import ModelForm

#from tagging_autocomplete_tagit.models import TagAutocompleteTagItField

NAME_MAXLEN=50

class Tag(models.Model):
    name = models.CharField(max_length=50, primary_key=True)

class CustomUserManager(models.Manager):
    def create_user(self, username, email):
        return self.model._default_manager.create(username=username)

class MyUser(models.Model):
    first_name = models.CharField(max_length=NAME_MAXLEN)
    last_name = models.CharField(max_length=NAME_MAXLEN)
    latitude = models.FloatField(default=40.344725)
    longitude = models.FloatField(default=-74.6556)
    
    username = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    objects = CustomUserManager()

    def is_authenticated(self):
        return True
    def __unicode__(self):
        return self.first_name + " " + self.last_name

class MyGroup(models.Model):
    users = models.ManyToManyField(MyUser, related_name="users")
    #creator = models.ForeignKey(MyUser, related_name="creator")
    creator = models.CharField(max_length=NAME_MAXLEN)
    name = models.CharField(max_length=NAME_MAXLEN)
    def __unicode__(self):
        return self.name

# Create your models here.
class NewEvent(models.Model):
    name = models.CharField(max_length=200)
    startTime = models.DateTimeField(default=datetime.date.today())
    endTime = models.DateTimeField(default=datetime.date.today())
    location = models.CharField(max_length=200, null=True, default="Princeton University")
    private = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    lat = models.DecimalField(max_digits=15, decimal_places=10, blank=True, null=True)
    lon = models.DecimalField(max_digits=15, decimal_places=10, blank=True, null=True)
    tags = models.ManyToManyField(Tag)
    #tags = models.CharField(max_length=200, blank=True, null=True, default="all")
    #tags = TagAutocompleteTagItField(max_tags=False)
    creator = models.ForeignKey(MyUser, related_name="creator", blank=True, null=True)
    groups = models.ManyToManyField(MyGroup, related_name="groups", blank=True, null=True)
    rsvp = models.ManyToManyField(MyUser, related_name="rsvp", blank=True, null=True)
    exported = models.NullBooleanField(default=False, null=True)
    def __unicode__(self):
        return self.name

class Invite(models.Model):
    event = models.ForeignKey(NewEvent)
    inviter = models.ForeignKey(MyUser, related_name="inviter")
    invitee = models.ForeignKey(MyUser, related_name="invitee")
    is_new = models.BooleanField(default=True)

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
    #start_tete = models.DateTimeField() start_tete..?
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    text = models.CharField(max_length=30)
    details = models.CharField(max_length=250)
