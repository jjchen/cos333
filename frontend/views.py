from django.shortcuts import redirect, render
from frontend.models import NewEvent
#from frontend.models import NewEventForm
from frontend.models import BuildingAlias
from frontend.models import MyUser
from frontend.models import MyGroup
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.db.models import Q
import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ModelForm

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
class NewEventForm(ModelForm):
	class Meta:
		model = NewEvent

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
		 #<a href="{% url 'frontend:rmgroup' g.0 %}">Remove</a>
		#for user in group.users:
		#	print user
		#print group.name
	#print inspect.getmembers(this_user)
#	print this_user.group_set.all()
	if request.method == 'POST':
		form = SettingsForm(request.POST) # A form bound to the POST data
		if form.is_valid():
			print "form is valid"
			return HttpResponseRedirect('/') # Redirect after POST
	else:
		
		form = SettingsForm(initial={'first_name': this_user.first_name,
									'last_name': this_user.last_name}) # An unbound form
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
			new_group.save()
			print form.cleaned_data
			return HttpResponseRedirect('/frontend/settings')
	else:
		form = AddgroupForm() # An unbound form
	return render(request, 'frontend/addgroup.html', {
        'form': form,
    })	
	return HttpResponseRedirect('/signup')

def rmgroup(request, group):
	print group
	try:
		group_obj = MyGroup.objects.get(name = group)
	except ObjectDoesNotExist:
		return HttpResponse('Tried removing non-existent group!', status=401)
	if group_obj.creator != request.user.username:
		return HttpResponse('Unauthorized access', status=401)
	group_obj.delete()
	return HttpResponseRedirect('/frontend/settings')

# Create your views here.
def index(request):
	# print "fwef" what is this?
	if request.method =='POST':
		query = request.POST['search_query']
		events_list = NewEvent.objects.filter(
			Q(name__icontains=query) | 
			Q(location__icontains=query)).order_by("date", "time")
		show_list = True
	else:
		events_list = NewEvent.objects.all().order_by("date", "time")
		show_list = False
	context = {'events_list': events_list, 'user': request.user, 
		   'show_list': show_list}
	username = request.user.username
	print "a"+username+"b"
	if username != "" and\
	 len(MyUser.objects.filter(user_id = username)) == 0:
		return HttpResponseRedirect('/signup')
	else: 
		return render(request, 'frontend/map.html', context)

def add(request):
	if request.method == 'POST':
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
								date = data['date'],
								time = data['time'],
								location = data['location'],
								lat = latitude,
								lon = longitude,
								tags = data['tags'])
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

def search(request):
	query = request.POST['search_query']

	results = NewEvent.objects.filter(Q(name__icontains=query) | 
					  Q(location__icontains=query))

	html = "<html><body>Search Results: %s" % query
	for event in results:
		html += "<br/> %s <br/>" % event.name
	html += "</body></html>"

	return HttpResponse(html)

