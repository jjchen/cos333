#entire file from http://copiesofcopies.org/webl/2010/04/26/a-better-datetime-widget-for-django/

from time import strptime, strftime 
from django import forms 
from django.db import models 
from django.forms import fields 
from widgets import JqSplitDateTimeWidget 
class JqSplitDateTimeField(fields.MultiValueField): 
    widget = JqSplitDateTimeWidget 
    def __init__(self, *args, **kwargs): 
        """ 
        Have to pass a list of field types to the constructor, else we won't 
        get any data to our compress method. """ 
        all_fields = ( fields.CharField(max_length=10), 
                       fields.CharField(max_length=2), 
                       fields.CharField(max_length=2), 
                       fields.ChoiceField(choices=[('AM','AM'),('PM','PM')])
                       ) 
        super(JqSplitDateTimeField, self).__init__(all_fields, *args, **kwargs) 
    
    def validate(self, value):
        print value

    def compress(self, data_list): 
        print "in compress fields"
        """ 
        Takes the values from the MultiWidget and passes them as a list to this 
        function. This function needs to compress the list into a single object 
        to save. 
        """ 
        if data_list: 
            if not (data_list[0] and data_list[1] and data_list[2] and \
                        data_list[3]): 
                raise forms.ValidationError("Field is missing data.") 
            try:    
                input_time = strptime("%s:%s %s"%(data_list[1], data_list[2], 
                                                    data_list[3]), "%I:%M %p") 
            except:
                raise forms.ValidationError("Invalid date or time.")
            datetime_string = "%s %s" % (data_list[0], 
                                         strftime('%H:%M', input_time)) 
            return datetime_string 
        return None
