from datetime import datetime, timedelta

from frontend.models import NewEvent
#from frontend.models import NewEventForm
from frontend.models import BuildingAlias
from frontend.models import Building
from frontend.models import MyUser
from frontend.models import MyGroup
from frontend.models import Friends
from frontend.models import CalEvent
from django.forms.models import model_to_dict

# tagging things
from tagging.forms import TagField
from tagging.models import Tag
#from tagging_autocomplete_tagit.widgets import TagAutocompleteTagIt

from django import forms
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db.models import Q

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render_to_response
from django.shortcuts import redirect, render
from django.template import RequestContext
from social_auth.models import UserSocialAuth
from facepy import GraphAPI
from facepy import SignedRequest
from fields import JqSplitDateTimeField
from widgets import JqSplitDateTimeWidget
from django.core.serializers.json import DjangoJSONEncoder
import json
import operator
import django.contrib.auth
import unicodedata

MAX_LEN = 50
class SignupForm(forms.Form):
	first_name = forms.CharField(max_length = MAX_LEN)
	last_name = forms.CharField(max_length = MAX_LEN)

class SettingsForm(forms.Form):
	first_name = forms.CharField()
	last_name = forms.CharField()
	latitude = forms.DecimalField()
	longitude = forms.DecimalField()

# makes a Form class from the NewEvent model
class NewEventForm(forms.Form):
	name = forms.CharField(max_length=200)
	startTime =  JqSplitDateTimeField(widget=JqSplitDateTimeWidget(
			attrs={'date_class':'datepicker',
			       'time_class':'timepicker'}))
	endTime =  JqSplitDateTimeField(widget=JqSplitDateTimeWidget(
			attrs={'date_class':'datepicker',
			       'time_class':'timepicker'}))
	location = forms.CharField(max_length=200)
	description = forms.CharField(required=False, widget=forms.Textarea)
	private = forms.BooleanField(required=False)
	groups = forms.ModelMultipleChoiceField(queryset=MyGroup.objects.all(),
						required=False)
	#tags = forms.CharField(max_length=200, required=False)
	#tags = TagField(widget=TagAutocompleteTagIt(max_tags=False))

# testing JSON autocomplete
def get_names(request):
	if request.is_ajax():
		q = request.GET.get('term', '')
		names = NewEvent.objects.filter(name__icontains = q)[:20]
		results = []
		for name in names:
			name_json = {}
			name_json['label'] = name.name
			results.append(name_json)
		data = json.dumps(results)
	else:
		data = 'fail'
	mimetype = 'application/json'
	return HttpResponse(data, mimetype)

def settings(request):
	if request.user.username == "":
		return HttpResponse('Unauthorized access--you must sign in!', 
						status=401)
	this_user = MyUser.objects.get(user_id = request.user.username)
	#if len(MyGroup.objects.all()) > 0:
	groups = MyGroup.objects.filter(creator = request.user.username)
	#groups = []
	group_info = []
	for group in groups:
		all_users = group.users.all()
		info = group.name + ": "
		for user in all_users:
			info += user.user_id + " "
		group_info.append((group.name, info))

	if request.method == 'POST':
		form = SettingsForm(request.POST)
		if form.is_valid():
			print "form is valid"
			data = form.cleaned_data
			this_user.first_name = data['first_name']
			this_user.last_name = data['last_name']
			this_user.latitude = data['latitude']
			this_user.longitude = data['longitude']
			this_user.save()
			this_user = MyUser.objects.get(
				user_id = request.user.username)
			print this_user.latitude
			return HttpResponseRedirect('/') # Redirect after POST
	else:
		form = SettingsForm(
			initial={'first_name': this_user.first_name,
				 'last_name': this_user.last_name,
				 'latitude': this_user.latitude,
				 'longitude': this_user.longitude})
	print "I am here, settings"
	return render(request, 'frontend/settings.html', {
        'form': form, 'group_info': group_info
	})

def signup(request):
	if request.method == 'POST':
		form = SignupForm(request.POST) # A form bound to the POST data
		if form.is_valid():
			data = form.cleaned_data
			user = MyUser(first_name = data['first_name'],
								last_name = data['last_name'],
								user_id = request.user.username)
			user.save()
			return HttpResponseRedirect('/') # Redirect after POST
	else:
		form = SignupForm() # An unbound form
	return render(request, 'frontend/signup.html', {
        'form': form,
    })

class MultiNameField(forms.CharField):
	def __init__(self):
		super(MultiNameField, self).__init__(widget=forms.TextInput())
	def to_python(self, value):
		if not value: return []
		return value.split(',')

	def validate(self, value):
		for name in value:
			if len(MyUser.objects.filter(user_id = name)) == 0:
				raise ValidationError("User " + name + " doesn't exist!")

def check_group_name(name):
	if len(MyGroup.objects.filter(name = name)) != 0:
		raise ValidationError("MyGroup name already taken!")

class AddgroupForm(forms.Form):
	#member_names = forms.CharField(widget=forms.Textarea(),
	#							validators=[validate_names])
	group_name = forms.CharField(validators=[check_group_name])
	member_names = MultiNameField()

class AddfriendsForm(forms.Form):
	#member_names = forms.CharField(widget=forms.Textarea(),
	#							validators=[validate_names])
	name = forms.CharField()

class SearchForm(forms.Form):
	search_query = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Search'}))

def addgroup(request):
	#print request.user.username
	#print MyUser.objects.get(user_id="foo")
	print "Request is " + request.user.username
	if request.user.username == "":
		return HttpResponse('Unauthorized access', status=401)
	if request.method == 'POST':
		form = AddgroupForm(request.POST) # A form bound to the POST data
		if form.is_valid():
			this_user = MyUser.objects.get(user_id = 
						       request.user.username)
			new_group = MyGroup()
			new_group.creator = this_user.user_id
			new_group.name = form.cleaned_data['group_name']
			new_group.save()
			print form.cleaned_data
			for name in form.cleaned_data['member_names']:
				user = MyUser.objects.get(user_id = name)
				new_group.users.add(user)
			new_group.users.add(this_user)
			new_group.save()
			return HttpResponseRedirect('/frontend/personal')
	return HttpResponseRedirect('/frontend/personal')

def addfriend(request):
	#print request.user.username
	#print MyUser.objects.get(user_id="foo")
	print "Request is " + request.user.username
	if request.user.username == "":
		return HttpResponse('Unauthorized access', status=401)
	if request.method == 'POST':
		form = AddfriendsForm(request.POST) # A form bound to the POST data
		if form.is_valid():
			print form.cleaned_data['name']
			this_user = MyUser.objects.get(user_id = request.user.username)
			try: 
				friends_obj = Friends.objects.get(name = this_user)
			except ObjectDoesNotExist:
				friends_obj = Friends()
				friends_obj.name = this_user
				friends_obj.save()
			name = form.cleaned_data['name']
			try: 
				user = MyUser.objects.get(user_id = name)
				friends_obj.friends.add(user)
			except ObjectDoesNotExist:
				# error!!
				print "ERROR: FRIEND NOT FOUND"
			friends_obj.save()
			return HttpResponseRedirect('/frontend/personal')
	return HttpResponseRedirect('/frontend/personal')
#	else:
#		form = AddfriendForm() # An unbound form
#	return render(request, 'frontend/personal.html', {
 #       'form': form,
  #  })	
	return HttpResponseRedirect('/signup')	

def rmfriend(request, user):
	try:
		remove_obj = MyUser.objects.get(id = user)
	except ObjectDoesNotExist:
		return HttpResponse('Tried removing non-existent friend!', status=401) 
	this_user = MyUser.objects.get(user_id = request.user.username)
	try: 
		friend_obj = Friends.objects.get(name = this_user)
	except ObjectDoesNotExist:
		return HttpResponseRedirect('/frontend/personal')			
	friend_obj.friends.remove(remove_obj)
	friend_obj.save()
	return HttpResponseRedirect('/frontend/personal')

def rmgroup(request, group):
	print group
	try:
		group_obj = MyGroup.objects.get(id = group)
	except ObjectDoesNotExist:
		return HttpResponse('Tried removing non-existent group!', status=401)
	#if group_obj.creator != request.user.username:
	#	return HttpResponse('Unauthorized access', status=401)
	#group_obj.delete()
	this_user = MyUser.objects.get(user_id = request.user.username)
	group_obj.users.remove(this_user)
	group_obj.save()
	return HttpResponseRedirect('/frontend/personal')

def rmevent(request, event):
	try:
		event_obj = NewEvent.objects.get(id = event)
	except ObjectDoesNotExist:
		return HttpResponse('Tried removing non-existent event!', 
				    status=401)
	this_user = MyUser.objects.get(user_id = request.user.username)
	if event_obj.creator != this_user:
		return HttpResponse('Unauthorized access', status=401)
	event_obj.delete()
	return HttpResponseRedirect('/frontend/personal')	

# export event to Facebook
def process_export(user, event_obj):
	#user and event_obj are MyUser and NewEvent type, respectively. Returns
	#True on success, False on failure
        instance = UserSocialAuth.objects.get(
		user=user, provider='facebook')        
        token = instance.tokens['access_token']
        graph = GraphAPI(token)
        if event_obj.private:
		privacy_type = "SECRET"
	else:
		privacy_type = "OPEN"
        event_path = str(instance.uid) + "/events"
        event_data = {
            'name' : event_obj.name,
            'start_time' : event_obj.startTime.isoformat(),
	    'end_time': event_obj.endTime.isoformat(),
            'location' : event_obj.location,
            'privacy_type' : privacy_type
            }
	print event_data
        result = graph.post(path=event_path, **event_data)
        print "Result: " + str(result)
        if result.get('id', False):
		return True
	else:
		return False

def exportevent(request, event):
	try:
		event_obj = NewEvent.objects.get(id = event)
	except ObjectDoesNotExist:
		return HttpResponse('Tried exporting non-existent event!', 
				    status=401)
	this_user = MyUser.objects.get(user_id = request.user.username)
	if event_obj.creator != this_user:
		return HttpResponse('Unauthorized access', status=401)
	success = process_export(this_user, event_obj)
	if success:
		return HttpResponseRedirect('/frontend/personal')
	return HttpResponse('Export failed!', status=401)


def addrsvp(request):
	if request.method == 'POST':
		this_user = MyUser.objects.get(user_id = request.user.username)
		try:
			id = request.POST.get('rsvp_id')

			event_obj = NewEvent.objects.get(id = id)
		except ObjectDoesNotExist:
			return HttpResponse('Tried rspving to non-existent group!', status=401)
		event_obj.rsvp.add(this_user)
		event_obj.save()
		return HttpResponse('{"success":"true"}');
	else:
		raise Http404('Unauthorized access');

def personal_ajax(request, event):
	if request.method == 'POST':
		try:
			event_obj = NewEvent.objects.get(id = event)
		except ObjectDoesNotExist:
			return HttpResponse('event does not exist!', status=401)
		return render_to_response('frontend/showevent.html', {'event' : event_obj}, context_instance=RequestContext(request))

def editevent(request, event):
	if request.method == 'POST':
		try:
			event_obj = NewEvent.objects.get(id = event)
			dictionary = model_to_dict(event_obj)
			form = NewEventForm(dictionary) # A form bound to data
		except ObjectDoesNotExist:
			return HttpResponse('Event does not exist!', status=401)
		return render_to_response('frontend/editevent.html',
	                              {'form' : form},
	                                context_instance=RequestContext(request))

def editgroup(request, group):
	#print request.user.username
	#print MyUser.objects.get(user_id="foo")
	if request.user.username == "":
		return HttpResponse('Unauthorized access', status=401)
	if request.method == 'POST':
		try:
			new_group = MyGroup.objects.get(id = group)
			for name in form.cleaned_data['member_names']:
				user = MyUser.objects.get(user_id = name)
				new_group.users.add(user)
			new_group.users.add(this_user)
			new_group.save()
		except ObjectDoesNotExist:
			return HttpResponse('Group does not exist!', status=401)
		return render_to_response('frontend/editgroup.html',
	                              {'form' : form},
	                                context_instance=RequestContext(request))

def rmrsvp(request, id=None):
	if request.method == 'POST':
		this_user = MyUser.objects.get(user_id = request.user.username)
		try:
			if (id == None):
				id = request.POST.get('rsvp_id')
			event_obj = NewEvent.objects.get(id = id)
		except ObjectDoesNotExist:
			return HttpResponse('Tried rspving to non-existent event!', status=401)
		event_obj.rsvp.remove(this_user)
		event_obj.save()
		return HttpResponse('{"success":"true"}');
	else:
		this_user = MyUser.objects.get(user_id = request.user.username)
		print id
		try:
			event_obj = NewEvent.objects.get(id = id)
		except ObjectDoesNotExist:
			return HttpResponse('Tried rspving to non-existent event!', status=401)
		event_obj.rsvp.remove(this_user)
		event_obj.save()
	return HttpResponseRedirect('/frontend/personal')	

def logout(request):
	django.contrib.auth.logout(request)
	return HttpResponseRedirect("/frontend")

def personal(request):
	print "Request is " + request.user.username
	if request.user.username == "":
		return HttpResponse('Unauthorized access', status=401)
	this_user = MyUser.objects.get(user_id = request.user.username)
#	groups = MyGroup.objects.filter(creator = request.user.username)
	#groups = this_user.users_set.all()
	groups = MyGroup.objects.filter(users = this_user)
	group_info = []
	for group in groups:
		all_users = group.users.all()
		info = group.name + ": "
		for user in all_users:
			info += user.user_id + " "
		group_info.append((group.id, info))
	my_events = NewEvent.objects.filter(creator = this_user)
	rsvped = NewEvent.objects.filter(rsvp = this_user)
	recommended = []

	all_users_obj =  MyUser.objects.all()
	all_users = [unicodedata.normalize('NFKD', user.user_id).encode('ascii', 'ignore') for user in all_users_obj]
	friends = []
	try: 
		friends_obj = Friends.objects.get(name = this_user)
		friends = friends_obj.friends.all()
		if (len(friends) != 0 and len(groups) != 0):
			recommended = NewEvent.objects.filter((reduce(operator.or_, (Q(rsvp=x) | Q(creator=x) for x in friends))) | (reduce(operator.or_, (Q(groups=x) for x in groups))))
		elif (len(friends) != 0): 
			recommended = NewEvent.objects.filter((reduce(operator.or_, (Q(rsvp=x) | Q(creator=x) for x in friends))))
		elif (len(groups) != 0):
			recommended = NewEvent.objects.filter((reduce(operator.or_, (Q(groups=x) for x in groups))))
		other_users = all_users_obj.exclude(pk__in = friends)
	except ObjectDoesNotExist:
		friends_obj = Friends()
		friends_obj.name = this_user
		friends_obj.save()
		other_users = all_users_obj

	events_list = list(my_events)
	events_list.extend(rsvped)
	events_list.extend(recommended);
	form = AddgroupForm() # An unbound form
	form2 = AddfriendsForm()
	return render(request, 'frontend/personal.html', {
        'form': form, 'form2':form2, 'group_info': group_info, 
	'my_events': my_events, 'rsvped': rsvped, 
        'events_list': events_list, 'recommended':recommended, 
	"friends":friends, 'other_users': other_users, 'all_users': all_users 
    })	

def filter(request):
	tags = request.POST.getlist('tags')
	personal_type = request.POST.get('type')
	search = request.POST.get('search_query')
	events_list = []
	context = {'events_list': events_list, 'user': request.user, 'rsvped': [],'tags': tags, 'cal_events': []}
	username = request.user.username
	print username
	if username != "" and\
	 len(MyUser.objects.filter(user_id = username)) == 0:
		return HttpResponseRedirect('/signup')
	else:
		try:
			user = MyUser.objects.get(user_id=username)
			print user
			lat = user.latitude
			lon = user.longitude
			context['rsvped'] = NewEvent.objects.filter(rsvp = user)
		except MyUser.DoesNotExist:
			user = None
			latitude = MyUser._meta.get_field_by_name('latitude')
			longitude = MyUser._meta.get_field_by_name('longitude')
			lat = latitude[0].default
			lon = longitude[0].default
		context['center_lat'] = lat
		context['center_lon'] = lon
	time_threshold = datetime.now() - timedelta(days = 1)
	if search != None:
		print "search"
		form = SearchForm(request.POST)
		if form.is_valid():
			print "valid"
			query = form.cleaned_data['search_query']
			events_list = NewEvent.objects.filter(
				Q(name__icontains=query) | 
				Q(location__icontains=query)).order_by("startTime")
			print events_list
			show_list = True
	elif tags != None and len(tags) != 0:
		events_list = NewEvent.objects.filter(reduce(operator.or_, (Q(tags__icontains=x) for x in tags)))
		show_list = False
	elif personal_type != None:
		if personal_type == 'recommended':
			if user == None:
				events_list = NewEvent.objects.all()
			else: 
				try: 
					friends_obj = Friends.objects.get(name = user)
					friends = friends_obj.friends.all()
					groups = MyGroup.objects.filter(users = user)

					if (len(friends) != 0 and len(groups) != 0):
						events_list = NewEvent.objects.filter((reduce(operator.or_, (Q(rsvp=x) | Q(creator=x) for x in friends))) | (reduce(operator.or_, (Q(groups=x) for x in groups))))
					elif (len(friends) != 0): 
						events_list = NewEvent.objects.filter((reduce(operator.or_, (Q(rsvp=x) | Q(creator=x) for x in friends))))
					elif (len(groups) != 0):
						events_list = NewEvent.objects.filter((reduce(operator.or_, (Q(groups=x) for x in groups))))					
				except ObjectDoesNotExist:
					friends_obj = Friends()
					friends_obj.name = this_user
					friends_obj.save()
		if personal_type == 'my_events':
			if user == None:
				events_list = []
			else:
				events_list = NewEvent.objects.filter(Q(creator = user) | Q(rsvp = user))
	else:
		events_list = NewEvent.objects.filter(startTime__gt=time_threshold).order_by("startTime")
		show_list = False	

	context['events_list'] = events_list

	tags = ['cos', '333', 'music', 'needs', 'database', 'integration']
	cal_events = []
	for e in events_list:
		startTime = e.startTime.strftime("%s %s" % ("%Y-%m-%d", "%H:%M:%S"));
		if e.endTime != None: 
			endTime = e.endTime.strftime("%s %s" % ("%Y-%m-%d", "%H:%M:%S"));
			read_only = True
			cal_events.append({'start_date': startTime, 'end_date': endTime, 'text': e.name, 'readonly': read_only});
		context['cal_events'] = json.dumps(cal_events, cls=DjangoJSONEncoder);
	print "end"
	return render_to_response('frontend/list.html', context, context_instance=RequestContext(request))

# Create your views here.  index is called on page load.
def index(request, add_form=None):
	events_list = []
	show_list = False
	if request.method =='POST' and add_form==None:
		form = SearchForm(request.POST)
		formEvent = NewEventForm()
		if form.is_valid():
			query = form.cleaned_data['search_query']
			events_list = NewEvent.objects.filter(
				Q(name__icontains=query) | 
				Q(location__icontains=query)).order_by("startTime")
			show_list = True
	else:
		form = SearchForm()
		time_threshold = datetime.now() - timedelta(days = 1)
		events_list = NewEvent.objects.filter(startTime__gt=time_threshold).order_by("startTime")
		show_list = False
	#tags = ['cos', '333', 'music', 'needs', 'database', 'integration']
	tags = Tag.objects.all()

	context = {'events_list': events_list, 'user': request.user, 
		   'show_list': show_list, 'search_form': form, 'rsvped': [],'tags': tags, 'cal_events': []}
	if add_form == None: 
		context['form'] = NewEventForm()
		context['make_visible'] = False
	else: 
		context['form'] = add_form
		context['make_visible'] = True
	username = request.user.username

	cal_events = []
	for e in events_list:
		startTime = e.startTime.strftime("%s %s" % ("%Y-%m-%d", "%H:%M:%S"));
		if e.endTime != None:
			endTime = e.endTime.strftime("%s %s" % ("%Y-%m-%d", "%H:%M:%S"));
			read_only = True
			cal_events.append({'start_date': startTime, 'end_date': endTime, 'text': e.name, 'readonly': read_only});
		context['cal_events'] = json.dumps(cal_events, cls=DjangoJSONEncoder);

	if username != "" and\
	 len(MyUser.objects.filter(user_id = username)) == 0:
		return HttpResponseRedirect('/signup')
	else:
		try:
			user = MyUser.objects.get(user_id=username)
			lat = user.latitude
			lon = user.longitude
			context['rsvped'] = NewEvent.objects.filter(rsvp = user)
		except MyUser.DoesNotExist:
			latitude = MyUser._meta.get_field_by_name('latitude')
			longitude = MyUser._meta.get_field_by_name('longitude')
			lat = latitude[0].default
			lon = longitude[0].default
		context['center_lat'] = lat
		context['center_lon'] = lon
	return render(request, 'frontend/map.html', context)

# add a new event.  add is called when a new event is properly submitted.
def add(request):
	if request.user.username == "":
		return HttpResponse('Unauthorized access--you must sign in!', 
					status=401)		
	if request.method == 'POST':
		username = request.user.username
		this_user = MyUser.objects.get(user_id = username)
		form = NewEventForm(request.POST) 
		if form.is_valid():
			data = form.cleaned_data
			data['startTime'] = datetime.strptime(
				data['startTime'], "%Y-%m-%d %H:%M")
			data['endTime'] = datetime.strptime(
				data['endTime'], "%Y-%m-%d %H:%M")
			
			buildingAlias = BuildingAlias.objects.filter(alias=data['location'])
			latitude = None
			longitude = None
			if (buildingAlias):
				building = buildingAlias[0].building
				latitude = building.lat
				longitude = building.lon
			event = NewEvent(name = data['name'],
					 startTime = data['startTime'],
					 endTime = data['endTime'],
					 location = data['location'],
					 lat = latitude,
					 lon = longitude,
					 private = data['private'],
					 #tags = data['tags'],
					 creator = this_user)
							#creator = this_user)
			event.save() #must save before adding groups
			for group in data['groups']:
				event.groups.add(group)
			event.save() 
			return render(request, 'frontend/success.html',
				      {'event': event})			

	else:
		form = NewEvent()
		print "newform"
			# msg = "success!"
	print "I am here in add"
	events_list = NewEvent.objects.all().order_by("startTime") # this is to refresh the events list without page refresh.
	return render(request, '/frontend/map.html', {'form': form})

	
# this is the search for a new event.
def search(request):
	query = request.POST['search_query']

	results = NewEvent.objects.filter(Q(name__icontains=query) | 
					  Q(location__icontains=query))

	html = "<html><body>Search Results: %s" % query
	for event in results:
		html += "<br/> %s <br/>" % event.name
	html += "</body></html>"

	return HttpResponse(html)

# call this to refresh events list.
def refresh(request):
   events_list = NewEvent.objects.all().order_by("startTime")
   show_list = False
   form = SearchForm(request.POST)
   tags = ['cos', '333', 'music', 'needs', 'database', 'integration']
   context = {'events_list': events_list, 'user': request.user, 
		   'show_list': show_list, 'search_form': form, 'tags': tags}
   print "I am here in refresh"
   return render(request, 'frontend/map.html', context)


def eventsXML(request):
    """
    For now, return the whole event DB.
    """
    eventList = NewEvent.objects.all()

    return render_to_response('frontend/events.xml',
                              {'eventList' : eventList,},
                                mimetype="application/xhtml+xml")

def dataprocessor(request):
    """
    QueryDict data format:
    <QueryDict:{
    u'ids': [u'1295982759946'],
    u'1295982759946_id': [u'1295982759946'],
    u'1295982759946_end_date': [u'2011-01-11 00:05'],
    u'1295982759946_text': [u'New event'],
    u'1295982759946_start_date': [u'2011-01-11 00:00'],
    u'1295982759946_!nativeeditor_status': [u'inserted']
    }>

    Response Data format:

    <data>
       <action type="some" sid="r2" tid="r2" />
       <action type="some" sid="r3" tid="r3" />
    </data>


    type
    the type of the operation (update, insert, delete, invalid, error);
    sid
    the original row ID (the same as gr_id);
    tid
    the ID of the row after the operation (may be the same as gr_id,
    or some different one - it can be used during a new row adding,
    when a temporary ID, created on the client-side, is replaced with the ID,
    taken from the DB or by any other business rule).

    """
    responseList = []
    
    if request.method == 'POST':

        idList = request.POST['ids'].split(',')
        
        for id in idList:
            command = request.POST[id + '_!nativeeditor_status']
            if command == 'inserted':
                e = CalEvent()
                e.start_date = request.POST[id + '_start_date']
                e.end_date = request.POST[id + '_end_date']
                e.text = request.POST[id + '_text']
                e.details = 'Bogus for now'
                e.save()
                response = {'type' : 'insert',
                            'sid': request.POST[id + '_id'],
                            'tid' : e.id}

            elif command == 'updated':
                e = CalEvent(pk=request.POST[id + '_id'])
                e.start_date = request.POST[id + '_start_date']
                e.end_date = request.POST[id + '_end_date']
                e.text = request.POST[id + '_text']
                e.details = 'Bogus for now'
                e.save()
                response = {'type' : 'update',
                            'sid': e.id,
                            'tid' : e.id}

            elif command == 'deleted':
                 e = CalEvent(pk=request.POST[id + '_id'])
                 e.delete()
                 response = {'type' : 'delete',
                            'sid': request.POST[id + '_id'],
                            'tid' : '0'}
                
            else:
                 response = {'type' : 'error',
                            'sid': request.POST[id + '_id'],
                            'tid' : '0'}
                
            responseList.append(response)
            
    return render_to_response('frontend/dataprocessor.xml', {"responseList": responseList},
                                    mimetype="application/xhtml+xml")

def calendar(request):
    return render_to_response('frontend/calendar.html', {}, 
			      context_instance=RequestContext(request))
