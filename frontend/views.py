from datetime import datetime, timedelta

from frontend.models import NewEvent
#from frontend.models import NewEventForm
from frontend.models import BuildingAlias
from frontend.models import Building
from frontend.models import MyUser
from frontend.models import MyGroup
from frontend.models import Friends
from frontend.models import CalEvent
from frontend.models import Invite
from frontend.models import Tag
from django.forms.models import model_to_dict

# tagging things
#from tagging.forms import TagField
#from tagging.models import Tag
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
from fields import JqSplitDateTimeField
from widgets import JqSplitDateTimeWidget
from django.core.serializers.json import DjangoJSONEncoder
import json
import operator
import django.contrib.auth
import unicodedata
import facebook 

MAX_LEN = 50
class SignupForm(forms.Form):
	first_name = forms.CharField(max_length = MAX_LEN)
	last_name = forms.CharField(max_length = MAX_LEN)

class SettingsForm(forms.Form):
	first_name = forms.CharField()
	last_name = forms.CharField()
	latitude = forms.DecimalField()
	longitude = forms.DecimalField()

class InviteForm(forms.Form):
	event = forms.CharField()
	invitee = forms.CharField()
	inviter = forms.CharField()


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
	tags = forms.CharField(max_length=200, required=False, widget=forms.HiddenInput())
	#tags = TagField(widget=TagAutocompleteTagIt(max_tags=False))

def accessible(event, user):
	groups = MyGroup.objects.filter(users = user)
	print event.groups.all()
	return (event.private == False) #or len(groups & event.groups.all()) != 0

def invite(request):
	if request.method == 'POST':
		form = InviteForm(request.POST)
		print form
		if form.is_valid():
			print "valid invite"
			data = form.cleaned_data
			invite = Invite()
			try:
				event = NewEvent.objects.get(id = data['event'])
				invitee = MyUser.objects.get(username = data['invitee'])
				inviter = MyUser.objects.get(id = data['inviter'])
			except ObjectDoesNotExist:
				return HttpResponse("Doesn't Exist!", 401)
			invite.event = event
			invite.invitee = invitee
			invite.inviter = inviter
			invite.save()
		else: 
			print "NOT valid"
	return HttpResponseRedirect('/frontend/personal')

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

def get_memnames(request):
	if request.is_ajax():
		q = request.GET.get('term', '')
		names = MyUser.objects.filter(first_name__icontains = q)[:20]
		results = []
		for first_name in names:
			first_name_json = {}
			first_name_json['label'] = first_name.name
			results.append(first_name_json)
		data = json.dumps(results)
	else:
		data = 'fail'
	mimetype = 'application/json'
	return HttpResponse(data, mimetype)

def locdemo(request):
	print "in locdemo"
	if request.method == 'POST':
		print "posting"
		print request.POST

		form = SettingsForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			print data
			return HttpResponseRedirect('/') # Redirect after POST
	else:
		form = SettingsForm()
	return render(request, 'frontend/demo.html', {'default_lat': 40.35,
						      'default_lon': -74.656})

# needs fixin'
def get_tags(request):
	if request.is_ajax():
		q = request.GET.get('term', '')
		tags = NewEvent.objects.filter(tags__icontains = q)[:20]
		results = []
		for tag in tags:
			tag_json = {}
			tag_json['label'] = tag.tags
			results.append(tag_json)
		data = json.dumps(results)
	else:
		data = 'fail'
	mimetype = 'application/json'
	return HttpResponse(data, mimetype)		

def settings(request):
	if request.user.username == "":
		return HttpResponse('Unauthorized access--you must sign in!', 
						status=401)
	this_user = MyUser.objects.get(username = request.user.username)
	#if len(MyGroup.objects.all()) > 0:
	groups = MyGroup.objects.filter(creator = request.user.username)
	#groups = []
	group_info = []
	for group in groups:
		all_users = group.users.all()
		info = group.name + ": "
		for user in all_users:
			info += user.username + " "
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
				username = request.user.username)
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
				      username = request.user.username)
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
			if len(MyUser.objects.filter(username = name)) == 0:
				raise ValidationError("User " + name + " doesn't exist!")

def check_group_name(name):
	if len(MyGroup.objects.filter(name = name)) != 0:
		raise ValidationError("MyGroup name already taken!")

class AddgroupForm(forms.Form):
	#member_names = forms.CharField(widget=forms.Textarea(),
	#							validators=[validate_names])
	group_name = forms.CharField()
	member_names = MultiNameField()

class AddfriendsForm(forms.Form):
	#member_names = forms.CharField(widget=forms.Textarea(),
	#							validators=[validate_names])
	name = forms.CharField()

class SearchForm(forms.Form):
	search_query = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Search'}))

def addgroup(request):
	#print request.user.username
	print "addgroup is " + request.user.username
	if request.user.username == "":
		return HttpResponse('Unauthorized access', status=401)
	if request.method == 'POST':
		print "post"
		form = AddgroupForm(request.POST) # A form bound to the POST data
		if form.is_valid():
			try: 
				old_group = MyGroup.objects.get(name=form.cleaned_data['group_name'])
				print "old group"
				for name in form.cleaned_data['member_names']:
					user = MyUser.objects.get(username = name)
					old_group.users.add(user)
				old_group.save()
				return HttpResponseRedirect('/frontend/personal')				
			except ObjectDoesNotExist:
				print "new group"

				this_user = MyUser.objects.get(username = 
							       request.user.username)
				new_group = MyGroup()
				new_group.creator = this_user.username
				new_group.name = form.cleaned_data['group_name']
				new_group.save()
				print form.cleaned_data
				for name in form.cleaned_data['member_names']:
					user = MyUser.objects.get(username = name)
					new_group.users.add(user)
				new_group.users.add(this_user)
				new_group.save()
				return HttpResponseRedirect('/frontend/personal')
		else:
			print "not valid"
	return HttpResponseRedirect('/frontend/personal')

def addfriend(request):
	#print request.user.username
	print "Request is " + request.user.username
	if request.user.username == "":
		return HttpResponse('Unauthorized access', status=401)
	if request.method == 'POST':
		form = AddfriendsForm(request.POST) # A form bound to the POST data
		if form.is_valid():
			print form.cleaned_data['name']
			this_user = MyUser.objects.get(username = request.user.username)
			try: 
				friends_obj = Friends.objects.get(name = this_user)
			except ObjectDoesNotExist:
				friends_obj = Friends()
				friends_obj.name = this_user
				friends_obj.save()
			name = form.cleaned_data['name']
			try: 
				user = MyUser.objects.get(username = name)
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
	return HttpResponseRedirect('/')	

def rmfriend(request, user):
	try:
		remove_obj = MyUser.objects.get(id = user)
	except ObjectDoesNotExist:
		return HttpResponse('Tried removing non-existent friend!', status=401) 
	this_user = MyUser.objects.get(username = request.user.username)
	try: 
		friend_obj = Friends.objects.get(name = this_user)
	except ObjectDoesNotExist:
		return HttpResponseRedirect('/frontend/personal')			
	friend_obj.friends.remove(remove_obj)
	friend_obj.save()
	return HttpResponseRedirect('/frontend/personal')
	

def rmgroup(request, group):
	try:
		group_obj = MyGroup.objects.get(id = group)
	except ObjectDoesNotExist:
		return HttpResponse('Tried removing non-existent group!', status=401)
	#if group_obj.creator != request.user.username:
	#	return HttpResponse('Unauthorized access', status=401)
	#group_obj.delete()
	this_user = MyUser.objects.get(username = request.user.username)
	group_obj.users.remove(this_user)
	group_obj.save()
	return HttpResponseRedirect('/frontend/personal')

def rmevent(request, event):
	try:
		event_obj = NewEvent.objects.get(id = event)
	except ObjectDoesNotExist:
		return HttpResponse('Tried removing non-existent event!', 
				    status=401)
	this_user = MyUser.objects.get(username = request.user.username)
	if event_obj.creator != this_user:
		return HttpResponse('Unauthorized access', status=401)
	event_obj.delete()
	return HttpResponseRedirect('/frontend/personal')	

def addrsvp(request):
	print "in rsvp"
	if request.method == 'POST':
		this_user = MyUser.objects.get(username = request.user.username)
		try:
			id = request.POST.get('rsvp_id')

			event_obj = NewEvent.objects.get(id = id)
			if (not accessible(event_obj, this_user)):
				return HttpResponse('You dont have access to this event!', status=401)
		except ObjectDoesNotExist:
			return HttpResponse('Tried rspving to non-existent group!', status=401)
		event_obj.rsvp.add(this_user)
		event_obj.save()
		print "saved"
		if request.POST.get('personal') == None:
			return HttpResponse('{"success":"true"}');
		else:
			return HttpResponseRedirect('/frontend/personal')
	else:
		raise Http404('Unauthorized access');

def personal_ajax(request, event):
	if request.method == 'POST':
		try:
			this_user = MyUser.objects.get(username = request.user.username)
			event_obj = NewEvent.objects.get(id = event)
			form = InviteForm(initial={'event': event, 'inviter': this_user.id})
			if (not accessible(event_obj, this_user)):
				return HttpResponse('You dont have access to this event!', status=401)
		except ObjectDoesNotExist:
			return HttpResponse('event does not exist!', status=401)
		return render_to_response('frontend/showevent.html', {'event' : event_obj, 'invite_form': form}, context_instance=RequestContext(request))

def editevent(request, event):
	if request.method == 'POST':
		try:
			event_obj = NewEvent.objects.get(id = event)
			dictionary = model_to_dict(event_obj)
			form = NewEventForm(initial=dictionary) # A form bound to data
		except ObjectDoesNotExist:
			return HttpResponse('Event does not exist!', status=401)
		return render_to_response('frontend/editevent.html',
	                              {'form' : form},
	                                context_instance=RequestContext(request))

def editgroup(request, group):
	#print request.user.username
	if request.user.username == "":
		return HttpResponse('Unauthorized access', status=401)
	if request.method == 'POST':
		try:
			new_group = MyGroup.objects.get(id = group)
			for name in form.cleaned_data['member_names']:
				user = MyUser.objects.get(username = name)
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
		this_user = MyUser.objects.get(username = request.user.username)
		try:
			if (id == None):
				id = request.POST.get('rsvp_id')
			event_obj = NewEvent.objects.get(id = id)
			if (not accessible(event_obj, this_user)):
				return HttpResponse('You dont have access to this event!', status=401)
		except ObjectDoesNotExist:
			return HttpResponse('Tried rspving to non-existent event!', status=401)
		event_obj.rsvp.remove(this_user)
		event_obj.save()
		return HttpResponse('{"success":"true"}');
	else:
		this_user = MyUser.objects.get(username = request.user.username)
		print id
		try:
			event_obj = NewEvent.objects.get(id = id)
			if (not accessible(event_obj, this_user)):
				return HttpResponse('You dont have access to this event!', status=401)
		except ObjectDoesNotExist:
			return HttpResponse('Tried rspving to non-existent event!', status=401)
		event_obj.rsvp.remove(this_user)
		event_obj.save()
	return HttpResponseRedirect('/frontend/personal')	

def logout(request):
	django.contrib.auth.logout(request)
	return HttpResponseRedirect("/frontend")

def removenew(request):
	if request.method == 'POST':
		try:
			this_user = MyUser.objects.get(username = request.user.username)
			invites = Invite.objects.filter(invitee = this_user)
			for invite in invites:
				invite.is_new = False;
				invite.save();
		except ObjectDoesNotExist:
				return HttpResponse('Tried rspving to non-existent event!', status=401)		
		return HttpResponse('{"success":"true"}');
	else:
		return HttpResponse('{"success":"true"}');

def personal(request):
	print "Request is " + request.user.username
	if request.user.username == "":
		return HttpResponse('Unauthorized access', status=401)
	this_user = MyUser.objects.get(username = request.user.username)
#	groups = MyGroup.objects.filter(creator = request.user.username)
	#groups = this_user.users_set.all()
	groups = MyGroup.objects.filter(users = this_user)
	invites = Invite.objects.filter(invitee = this_user)
	my_events = NewEvent.objects.filter(Q(creator = this_user), (Q(private = False) | Q(groups__in=groups))).order_by("startTime")
	rsvped = NewEvent.objects.filter(rsvp = this_user).order_by("startTime")
	recommended = []
	all_users_obj =  MyUser.objects.all()
	all_users = [unicodedata.normalize('NFKD', user.username).encode('ascii', 'ignore') for user in all_users_obj]
	friends = []
	try: 
		friends_obj = Friends.objects.get(name = this_user)
		friends = friends_obj.friends.all()
		if (len(friends) != 0 and len(groups) != 0):
			recommended = NewEvent.objects.filter(((reduce(operator.or_, (Q(rsvp=x) 
				| Q(creator=x) for x in friends))) | (reduce(operator.or_, (Q(groups=x) for x in groups)))), (Q(private = False) 
				| Q(groups__in=groups)))
		elif (len(friends) != 0): 
			recommended = NewEvent.objects.filter((reduce(operator.or_, (Q(rsvp=x) 
				| Q(creator=x) for x in friends))), (Q(private = False) 
				| Q(groups__in=groups)))
		elif (len(groups) != 0):
			recommended = NewEvent.objects.filter((reduce(operator.or_, (Q(groups=x) for x in groups))), (Q(private = False) 
				| Q(groups__in=groups)))
		if len(recommended) != 0:
			recommended = recommended.filter(~Q(rsvp=this_user)).order_by("startTime")

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
	fb_groups = facebook.get_fb_groups(request)
	fb_friends = facebook.get_friends(request)
	return render(request, 'frontend/personal.html', {
        'form': form, 'form2':form2, 'groups_list': groups, 'my_events': my_events, 'rsvped': rsvped, 
        'events_list': events_list, 'recommended':recommended, "friends":friends, 
        'other_users': other_users, 'all_users': all_users, 'fb_groups': fb_groups, 'fb_friends': fb_friends, 'invites':invites
    })	


def filter(request):
	tags = request.POST.getlist('tags')
	personal_type = request.POST.get('type')
	search = request.POST.get('search_query')
	events_list = []
	context = {'events_list': events_list, 'user': request.user, 'rsvped': [],'tags': tags, 'cal_events': []}
	username = request.user.username
	groups = []
	print username
	if username != "" and\
	 len(MyUser.objects.filter(username = username)) == 0:
		return HttpResponseRedirect('/signup')
	else:
		try:
			user = MyUser.objects.get(username=username)
			invites = Invite.objects.filter(invitee = user)
			print user
			lat = user.latitude
			lon = user.longitude
			groups = MyGroup.objects.filter(users = user)
			context['rsvped'] = NewEvent.objects.filter(Q(rsvp = user), (Q(private = False) | Q(groups__in=groups)))
		except MyUser.DoesNotExist:
			user = None
			latitude = MyUser._meta.get_field_by_name('latitude')
			longitude = MyUser._meta.get_field_by_name('longitude')
			lat = latitude[0].default
			lon = longitude[0].default
			invites = []
		context['invites'] = invites
		context['center_lat'] = lat
		context['center_lon'] = lon
	time_threshold = datetime.now() - timedelta(days = 1)
	if search != None:
		print "search"
		form = SearchForm(request.POST)
		if form.is_valid():
			print "valid"
			query = form.cleaned_data['search_query']
			try:
				user = MyUser.objects.get(username=username)
				try: 
					tags_list = [Tag.objects.get(name = query)]
					print "YESSS"
				except ObjectDoesNotExist:
					tags_list = []
				events_list = NewEvent.objects.filter(
					(Q(name__icontains=query) | 
					Q(location__icontains=query) | Q(tags__in=tags_list)), (Q(private = False) | Q(groups__in=groups))).order_by("startTime") 
			except ObjectDoesNotExist: 
				events_list = NewEvent.objects.filter(
					Q(name__icontains=query) | 
					Q(location__icontains=query) | Q(tags__in=query)).order_by("startTime")
			show_list = True
	elif tags != None and len(tags) != 0:
		tags_list = []
		groups_list = []
		for tag in tags:
			try:
				tags_list += [Tag.objects.get(name = tag)]
			except ObjectDoesNotExist:
				try:
					groups_list += [MyGroup.objects.get(name=tag)]
				except ObjectDoesNotExist:
					continue
		events_list = NewEvent.objects.filter((reduce(operator.or_, [Q(tags__in=tags_list) | Q(groups__in =groups_list)])), (Q(private = False) | Q(groups__in=groups)))
		show_list = False
	elif personal_type != None:
		if personal_type == 'recommended':
			if user == None:
				events_list = NewEvent.objects.filter(Q(private = False) | Q(groups__in=groups))
			else: 
				try: 
					friends_obj = Friends.objects.get(name = user)
					friends = friends_obj.friends.all()
					groups = MyGroup.objects.filter(users = user)

					if (len(friends) != 0 and len(groups) != 0):
						events_list = NewEvent.objects.filter(((reduce(operator.or_, (Q(rsvp=x) 
							| Q(creator=x) for x in friends))) | (reduce(operator.or_, (Q(groups=x) for x in groups)))), (Q(private = False) 
							| Q(groups__in=groups)))
					elif (len(friends) != 0): 
						events_list = NewEvent.objects.filter((reduce(operator.or_, (Q(rsvp=x) 
							| Q(creator=x) for x in friends))), (Q(private = False) | Q(groups__in=groups)))
					elif (len(groups) != 0):
						events_list = NewEvent.objects.filter((reduce(operator.or_, (Q(groups=x) for x in groups))), (Q(private = False) 
							| Q(groups__in=groups)))

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
		try:
			user = MyUser.objects.get(username=username)
			groups = MyGroup.objects.filter(users = user)
			events_list = NewEvent.objects.filter(Q(startTime__gt=time_threshold),(Q(private = False) | Q(groups__in=groups))).order_by("startTime")
		except ObjectDoesNotExist:
			events_list = NewEvent.objects.filter(Q(startTime__gt=time_threshold)).order_by("startTime")
		
		show_list = False	
	if len(events_list) != 0:
		events_list = events_list.order_by("startTime")
	context['events_list'] = events_list

	tags = ['cos', '333', 'music', 'needs', 'database', 'integration']
	cal_events = []
	description = ""
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
	all_buildings = Building.objects.all()
	location = [unicodedata.normalize('NFKD', building.name).encode('ascii', 'ignore') for building in all_buildings]

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
	tags = [unicodedata.normalize('NFKD', tag.name).encode('ascii', 'ignore') for tag in tags]

	context = {'events_list': events_list, 'user': request.user, 
		   'show_list': show_list, 'search_form': form, 'rsvped': [],'tags': tags, 'cal_events': [], 'locations': location}
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
	 len(MyUser.objects.filter(username = username)) == 0:
		return HttpResponseRedirect('/signup')
	else:
		try:
			#User exists
			user = MyUser.objects.get(username=username)
			lat = user.latitude
			lon = user.longitude
			context['rsvped'] = NewEvent.objects.filter(rsvp = user)
			groups = MyGroup.objects.filter(users = user)
		except MyUser.DoesNotExist:
			#User doesn't exist
			latitude = MyUser._meta.get_field_by_name('latitude')
			longitude = MyUser._meta.get_field_by_name('longitude')
			lat = latitude[0].default
			lon = longitude[0].default
			groups = []
		context['groups'] = groups
		context['center_lat'] = lat
		context['center_lon'] = lon
	context['logged_in'] = (username != "")
	return render(request, 'frontend/map.html', context)

# add a new event.  add is called when a new event is properly submitted.
def add(request):
	if request.user.username == "":
		return HttpResponse('Unauthorized access--you must sign in!', 
					status=401)		
	if request.method == 'POST':
		username = request.user.username
		this_user = MyUser.objects.get(username = username)
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
					 creator = this_user,
					 description = data['description'])
							#creator = this_user)
			event.save() #must save before adding groups
			# new tagging method
			tag_list = [Tag.objects.get_or_create(name=tag)[0] for tag in data['tags'].split()],
			for tag in tag_list:
				event.tags.add(*tag)
			#	event.tags.add(tag)
			# group stuff
			for group in data['groups']:
				event.groups.add(group)
			event.save() 
			return render(request, 'frontend/success.html',
				      {'event': event})			

	else:
		form = NewEvent()
		print "newform"
			# msg = "success!"
	events_list = NewEvent.objects.all().order_by("startTime") # this is to refresh the events list without page refresh.
	return render(request, '/frontend/map.html', {'form': form})

# add a new event.  add is called when a new event is properly submitted.
def edit(request, event):
	print "IN edit"
	if request.method == 'POST':

		if request.user.username == "":
			return HttpResponse('Unauthorized access--you must sign in!', 
						status=401)
		try:
			old_event = NewEvent.objects.get(id = event)
			username = request.user.username
			this_user = MyUser.objects.get(username = username)
			if old_event.creator != this_user:
				return HttpResponse('Unauthorized access', status=401)

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
				old_event.name = data['name']
				old_event.startTime = data['startTime']
				old_event.endTime = data['endTime']
				old_event.location = data['location']
				old_event.lat = latitude
				old_event.lon = longitude
				old_event.private = data['private']
				old_event.description = data['description']				
				old_event.save() #must save before adding groups
				for group in data['groups']:
					if not old_event.groups.filter(pk = group.pk):
						old_event.groups.add(group)
				old_event.save() 

				return HttpResponseRedirect('/frontend/personal')
			else:
				return HttpResponseRedirect('/frontend/personal')
		except ObjectDoesNotExist:
			return HttpResponse('Event does not exist', status=401)
	else:
		return HttpResponse('How did you get here?', 
						status=401)

	
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
