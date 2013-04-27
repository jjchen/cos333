from django.shortcuts import redirect, render
from frontend.models import NewEvent
#from frontend.models import NewEventForm
from frontend.models import BuildingAlias
from frontend.models import MyUser
from frontend.models import MyGroup
from frontend.models import Friends
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.db.models import Q
from datetime import datetime, timedelta
from django import forms
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ModelForm
from django.shortcuts import render_to_response
from frontend.models import CalEvent
from django.template import RequestContext

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
	startTime = forms.DateTimeField()
	endTime = forms.DateTimeField()
	location = forms.CharField(max_length=200)
	private = forms.BooleanField()
	groups = forms.ModelMultipleChoiceField(queryset=MyGroup.objects.all())
	
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
		super(MultiNameField, self).__init__(widget=forms.Textarea())
	def to_python(self, value):
		if not value: return []
		return value.replace('\r\n', '\n').split('\n')
	
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
	friends_names = MultiNameField()

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
			this_user = MyUser.objects.get(user_id = request.user.username)
			new_group = MyGroup()
			new_group.creator = this_user.user_id
			new_group.name = form.cleaned_data['group_name']
			new_group.save()
			print form.cleaned_data
			for name in form.cleaned_data['member_names']:
				print name
				user = MyUser.objects.get(user_id = name)
				new_group.users.add(user)
			new_group.users.add(this_user)
			new_group.save()
			print form.cleaned_data
			return HttpResponseRedirect('/frontend/personal')
	return HttpResponseRedirect('/frontend/personal')

	return HttpResponseRedirect('/signup')

def addfriend(request):
	#print request.user.username
	#print MyUser.objects.get(user_id="foo")
	print "Request is " + request.user.username
	if request.user.username == "":
		return HttpResponse('Unauthorized access', status=401)
	if request.method == 'POST':
		form = AddfriendsForm(request.POST) # A form bound to the POST data
		if form.is_valid():
			this_user = MyUser.objects.get(user_id = request.user.username)
			try: 
				friends_obj = Friends.objects.get(name = this_user)
			except ObjectDoesNotExist:
				friends_obj = Friends()
				friends_obj.name = this_user
				friends_obj.save()
			for name in form.cleaned_data['friends_names']:
				print name
				user = MyUser.objects.get(user_id = name)
				friends_obj.friends.add(user)
			friends_obj.save()
			return HttpResponseRedirect('/frontend/personal')
	return HttpResponseRedirect('/frontend/personal')
#	else:
#		form = AddfriendForm() # An unbound form
#	return render(request, 'frontend/personal.html', {
 #       'form': form,
  #  })	
	return HttpResponseRedirect('/signup')	

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
		event_obj = NewEvent.objects.get(name = event)
	except ObjectDoesNotExist:
		return HttpResponse('Tried removing non-existent event!', status=401)
	if event_obj.creator != request.user.username:
		return HttpResponse('Unauthorized access', status=401)
	event_obj.delete()
	return HttpResponseRedirect('/frontend/personal')	

def addrsvp(request, event):
	this_user = MyUser.objects.get(user_id = request.user.username)
	try:
		event_obj = NewEvent.objects.get(id = event)
	except ObjectDoesNotExist:
		return HttpResponse('Tried rspving to non-existent group!', status=401)
	event_obj.rsvp.add(this_user)
	event_obj.save()
	return HttpResponseRedirect('/')

def rmrsvp(request, event):
	this_user = MyUser.objects.get(user_id = request.user.username)

	try:
		event_obj = NewEvent.objects.get(id = event)
	except ObjectDoesNotExist:
		return HttpResponse('Tried rspving to non-existent group!', status=401)
	event_obj.rsvp.remove(this_user)
	event_obj.save()
	return HttpResponseRedirect(reverse('frontend:index'))

def logout(request):
	return HttpResponseRedirect(reverse('frontend:personal'))

def personal(request):
	print "Request is " + request.user.username
	if request.user.username == "":
		return HttpResponse('Unauthorized access', status=401)
	this_user = MyUser.objects.get(user_id = request.user.username)
#	groups = MyGroup.objects.filter(creator = request.user.username)
	# SHOULD ALSO FILTER BY MEMBERS? show groups i'm in, as well as groups i made
	#groups = this_user.users_set.all()
	groups = MyGroup.objects.filter(users = this_user)
	group_info = []
	for group in groups:
		all_users = group.users.all()
		info = group.name + ": "
		for user in all_users:
			info += user.user_id + " "
		group_info.append((group.id, info))
#	my_events = []
	my_events = NewEvent.objects.filter(creator = this_user)
#	rsvped = []
	rsvped = NewEvent.objects.filter(rsvp = this_user)
	#this_user.rsvp_set.all()
#	friends = []
	friends_obj = Friends.objects.get(name = this_user)
	friends = friends_obj.friends.all()

	recommended = []
#	friends rsvp, groups 
	for friend in friends:
		# get friends rsvp
		recommended += NewEvent.objects.filter(rsvp = friend)
		recommended += NewEvent.objects.filter(creator = friend)
	for group in groups:
		# group events
		recommended += NewEvent.objects.filter(groups = group)
	my_tags = []
#   
	form = AddgroupForm() # An unbound form
	form2 = AddfriendsForm()
	return render(request, 'frontend/personal.html', {
        'form': form, 'form2':form2, 'group_info': group_info, 'my_events': my_events, 'rsvped': rsvped, 'recommended':recommended, 'my_tags':my_tags, "friends":friends 
    })	

# Create your views here.  index is called on page load.
def index(request):
	# print "fwef" what is this?
	if request.method =='POST':
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
		tags = ['cos', '333', 'music', 'needs', 'database', 'integration']
	context = {'events_list': events_list, 'user': request.user, 
		   'show_list': show_list, 'search_form': form, 'form': NewEventForm(), 'tags': tags}
	username = request.user.username

	if username != "" and\
	 len(MyUser.objects.filter(user_id = username)) == 0:
		return HttpResponseRedirect('/signup')
	else:
		try:
			user = MyUser.objects.get(user_id=username)
			lat = user.latitude
			lon = user.longitude
		except MyUser.DoesNotExist:
			lat = MyUser.latitude.default
			lon = MyUser.longitude.default
		context['center_lat'] = lat
		context['center_lon'] = lon
	return render(request, 'frontend/map.html', context)
# add a new event.  add is called when a new event is properly submitted.
def add(request):
	if request.method == 'POST':
		username = request.user.username
		this_user = MyUser.objects.filter(user_id = username)
		form = NewEventForm(request.POST) # A form bound to the POST data
		if form.is_valid():
			data = form.cleaned_data
			buildingAlias = BuildingAlias.objects.filter(alias=data['location'])
			latitude = None
			longitude = None
			if (buildingAlias):
				building = buildingAlias[0].building
				latitude = building.lat
				longitude = building.lon
			event = NewEvent(name = data['name'],
					 startTime = data['startTime'],
							location = data['location'],
							lat = latitude,
							lon = longitude,
							tags = data['tags'])
							#creator = this_user)
			event.save()
			if request.is_ajax():
				return render(request, 'frontend/success.html')
			else:
				return redirect('success')
			# msg = "success!"
			# return HttpResponseRedirect('/') # Redirect after POST
	else:
		form = NewEventForm() # An unbound form
	return render(request, 'frontend/map.html', {'form': form})

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
def refreshEvents(request):
   events_list = NewEvent.objects.all().order_by("startTime")


def eventsXML(request):
    """
    For now, return the whole event DB.
    """
    eventList = CalEvent.objects.all()

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
    return render_to_response('frontend/calendar.html', {}, context_instance=RequestContext(request))
