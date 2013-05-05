import datetime
import time
import json
import urllib2

import xml.etree.ElementTree as ET
from django.core.management.base import BaseCommand, CommandError
from frontend.models import NewEvent

class Command(BaseCommand):
    def xml_tag(self, tag):
        return str(ET.QName('http://as.oit.princeton.edu/xml/events-1_0', tag))

    def handle(self, *args, **options):
        '''
        feeds = ["http://etcweb.princeton.edu/webfeeds/events/?fmt=json",
                 "http://etcweb.princeton.edu/webfeeds/events/roxen/?fmt=json",
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
        '''

        usg = "http://etcweb.princeton.edu/webfeeds/events/usg/?fmt=xml"
        resp = urllib2.urlopen(usg)
        xml_tree = ET.parse(resp)
        root = xml_tree.getroot()

        events = root.findall(self.xml_tag('event'))

        for e in events:
            print e.tag
            print ET.tostring(e)

            f_title = e.find(self.xml_tag('title')).text
            f_description = e.find(self.xml_tag('description')).text
            f_locationID = e.find(self.xml_tag('locationID')).text
            f_locationName = e.find(self.xml_tag('locationName')).text
            f_startDate = e.find(self.xml_tag('startDate')).text
            f_startTime = e.find(self.xml_tag('startTime')).text
            f_endDate = e.find(self.xml_tag('endDate')).text
            f_endTime = e.find(self.xml_tag('endTime')).text
            f_categories = e.find(self.xml_tag('categories')).text

            #f_description = event['description']
            #f_audience = event['audience']
            #f_tags = event['categories']['categoryName']

            # start date, time

            f_sDate = f_startDate.split()[0]
            sDate = datetime.datetime.strptime(f_sDate, "%Y-%m-%d").date()

            f_sTime = f_startTime.split()[0]

            sTime = datetime.datetime.strptime(f_sTime, "%H:%M:%S").time()
            startDateTime = datetime.datetime.combine(sDate, sTime)

            # end date, time
            f_eDate = f_endDate.split()[0]
            eDate = datetime.datetime.strptime(f_eDate, "%Y-%m-%d").date()

            f_eTime = f_endTime.split()[0]
            eTime = datetime.datetime.strptime(f_eTime, "%H:%M:%S").time()

            endDateTime = datetime.datetime.combine(eDate, eTime)

            # make into tags
            #categories = event['categories']
            
            new_event = NewEvent(name=f_title, startTime=startDateTime, endTime=endDateTime,
                                 location=f_locationName, lat=40.344725, lon=-74.6556, tags="")
            new_event.save()

    