import datetime
import time
import json
import urllib2

import xml.etree.ElementTree as ET
from django.core.management.base import BaseCommand, CommandError
from frontend.models import NewEvent

class Command(BaseCommand):
    def xml_tag(self, uri, tag):
        return str(ET.QName(uri, tag))

    def getCoordinates(self, locationName):
        url = "http://etcweb.princeton.edu/webfeeds/map/"
        resp = urllib2.urlopen(url)
        xml_tree = ET.parse(resp)
        root = xml_tree.getroot()

        print locationName

        # search 'official' names
        for location in root.iter('location'):
            if (location.find('name').text == locationName):
                f_latitude = location.find('latitude').text
                f_longitude = location.find('longitude').text
                return [float(f_latitude), float(f_longitude)]

        # search possible aliases
        # reiterate through locations to prevent conflicts
        for location in root.iter('location'):
            aliases = location.find('aliases')
            for alias in aliases.iter('alias'):
                if (location.find('name').text == locationName):
                    f_latitude = location.find('latitude').text
                    f_longitude = location.find('longitude').text
                    return [float(f_latitude), float(f_longitude)]

        return False

    def addEvent(self, uri, event, calendarName):
        e = event

        f_title = e.find(self.xml_tag(uri, 'title')).text
        #f_locationID = e.find(self.xml_tag(uri, 'locationID')).text
        f_locationName = e.find(self.xml_tag(uri, 'locationName')).text
        f_startDate = e.find(self.xml_tag(uri, 'startDate')).text
        f_startTime = e.find(self.xml_tag(uri, 'startTime')).text
        f_endDate = e.find(self.xml_tag(uri, 'endDate')).text
        f_endTime = e.find(self.xml_tag(uri, 'endTime')).text

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

        # search database for existing event; add if nonexistent
        f_event = NewEvent.objects.filter(name=f_title, location=f_locationName,
                                          startTime=startDateTime)
        
        if (len(f_event) > 0):
            return

        else:
            f_description = e.find(self.xml_tag(uri, 'description')).text
            f_categories = e.find(self.xml_tag(uri, 'categories')).text

            try:
                f_latitude = e.find(self.xml_tag(uri, 'latitude')).text
                f_longitude = e.find(self.xml_tag(uri, 'longitude')).text
            except:
                f_latitude = None
                f_longitude = None

            coordinates = self.getCoordinates(f_locationName)
            print coordinates

            if (coordinates != False):
                f_latitude = coordinates[0]
                f_longitude = coordinates[1]

            new_event = NewEvent(name=f_title, startTime=startDateTime, 
                                 endTime=endDateTime, location=f_locationName, 
                                 lat=f_latitude, lon=f_longitude, tags=calendarName,
                                 description = f_description)
            new_event.save()

    def handle(self, *args, **options):

        feeds = ["http://etcweb.princeton.edu/webfeeds/events/?fmt=xml",
                 "http://etcweb.princeton.edu/webfeeds/events/roxen/?fmt=xml",
                 "http://etcweb.princeton.edu/webfeeds/events/usg/?fmt=xml"]

        for url in feeds:
            resp = urllib2.urlopen(url)
            xml_tree = ET.parse(resp)
            root = xml_tree.getroot()

            if (root.tag[0] == "{"):
                uri = root.tag[1:].split("}")[0]
            else:
                continue

            events = root.findall(self.xml_tag(uri, 'event'))
            calendar = root.find(self.xml_tag(uri, 'calendarName'))
            calendarName = calendar.text

            for e in events:
                self.addEvent(uri, e, calendarName)
    