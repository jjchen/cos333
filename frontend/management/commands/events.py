import datetime
import time
import json
import urllib2

from django.core.management.base import BaseCommand, CommandError
from frontend.models import NewEvent

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        feeds = ["http://etcweb.princeton.edu/webfeeds/events/?fmt=json",
                 "http://etcweb.princeton.edu/webfeeds/events/roxen/?fmt=json",
                 "http://etcweb.princeton.edu/webfeeds/events/usg/?fmt=json",
                 "http://etcweb.princeton.edu/webfeeds/athletics/?fmt=json"]

        for url in feeds:
            resp = urllib2.urlopen(url)
            json_obj = json.load(resp)
            
            events = json_obj['events']
            
            for event in events:
                try:
                    NewEvent.objects.get(name = event['title'])

                except NewEvent.DoesNotExist:
                    print event
                    f_name = event['title']
                    f_building = event['locationName']
                    
                    try:
                        f_latitude = event['latitude']
                        break
                    except KeyError:
                        f_latitude = 0

                    try:
                        f_longitude = event['longitude']
                        break
                    except KeyError:
                        f_longitude = 0

                    f_startDate = event['startDate']
                    f_startTime = event['startTime']
                    f_endDate = event['endDate']
                    f_endTime = event['endTime']
                    #f_description = event['description']
                    #f_audience = event['audience']
                    #f_tags = event['categories']['categoryName']
                    print 1
                    print 'yeah'
                    # start date, time
                    print type(f_startDate)
                    sDate = datetime.datetime.strptime(f_startDate['0'], "%Y-%m-%d").date()
                    print 2
                    f_sTime = f_startTime.split()
                    sTime = datetime.datetime.strptime(f_sTime[0], "%H:%M:%S").time()
                    print 3
                    startDateTime = datetime.datetime.combine(sDate, sTime)
                    print 4
                    # end date, time
                    eDate  = datetime.datetime.strptime(f_endDate['0'], "%Y-%m-%d").date()
                    print 5
                    f_eTime = f_endTime.split()
                    eTime = datetime.datetime.strptime(f_eTime[0], "%H:%M:%S").time()
                    print 6
                    endDateTime = datetime.datetime.combine(eDate, eTime)
                    print 7
                    # make into tags
                    #categories = event['categories']
                    
                    new_event = NewEvent(name=f_name, startTime=startDateTime, endTime=endDateTime,
                                         location=f_building, lat=f_latitude, lon=f_longitude, tags="")
                    new_event.save()

    def handle(self, *args, **options):
        feeds = ["http://etcweb.princeton.edu/webfeeds/events/?fmt=json",
                 "http://etcweb.princeton.edu/webfeeds/events/roxen/?fmt=json",
                 "http://etcweb.princeton.edu/webfeeds/events/usg/?fmt=json",
                 "http://etcweb.princeton.edu/webfeeds/athletics/?fmt=json"]

        for url in feeds:
            resp = urllib2.urlopen(url)
            json_obj = json.load(resp)
            
            events = json_obj['events']
            
            for event in events:
                try:
                    NewEvent.objects.get(name = event['title'])

                except NewEvent.DoesNotExist:
                    print event
                    f_name = event['title']
                    f_building = event['locationName']
                    
                    try:
                        f_latitude = event['latitude']
                        break
                    except KeyError:
                        f_latitude = 0

                    try:
                        f_longitude = event['longitude']
                        break
                    except KeyError:
                        f_longitude = 0

                    f_startDate = event['startDate']
                    f_startTime = event['startTime']
                    f_endDate = event['endDate']
                    f_endTime = event['endTime']
                    #f_description = event['description']
                    #f_audience = event['audience']
                    #f_tags = event['categories']['categoryName']
                    print 1
                    print 'yeah'
                    # start date, time
                    print type(f_startDate)
                    sDate = datetime.datetime.strptime(f_startDate['0'], "%Y-%m-%d").date()
                    print 2
                    f_sTime = f_startTime.split()
                    sTime = datetime.datetime.strptime(f_sTime[0], "%H:%M:%S").time()
                    print 3
                    startDateTime = datetime.datetime.combine(sDate, sTime)
                    print 4
                    # end date, time
                    eDate  = datetime.datetime.strptime(f_endDate['0'], "%Y-%m-%d").date()
                    print 5
                    f_eTime = f_endTime.split()
                    eTime = datetime.datetime.strptime(f_eTime[0], "%H:%M:%S").time()
                    print 6
                    endDateTime = datetime.datetime.combine(eDate, eTime)
                    print 7
                    # make into tags
                    #categories = event['categories']
                    
                    new_event = NewEvent(name=f_name, startTime=startDateTime, endTime=endDateTime,
                                         location=f_building, lat=f_latitude, lon=f_longitude, tags="")
                    new_event.save()
