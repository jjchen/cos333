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