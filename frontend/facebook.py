from social_auth.models import UserSocialAuth
from facepy import GraphAPI
from frontend.models import MyUser
from frontend.models import MyGroup
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from frontend.models import NewEvent

# Facebook decorator to setup environment
def facebook_decorator(func):
    def wrapper(request, *args, **kwargs):
        user = request.user
        # User must me logged via FB backend in order to ensure we talk about 
        # the same person
        if not is_complete_authentication(request):
            try:
                user = social_complete(request, FacebookBackend.name)
            except ValueError:
                pass # no matter if failed

        # Not recommended way for FB, but still something we need to be aware of
        if isinstance(user, HttpResponse):
            kwargs.update({'auth_response': user})
        # Need to re-check the completion
        else:
            if is_complete_authentication(request):
                token = get_access_token(request.user)
                kwargs.update({'access_token': token})
                graph = GraphAPI(token)
                kwargs.update({'graph': graph})
            else:
                request.user = AnonymousUser()

        signed_request = load_signed_request(
            request.REQUEST.get('signed_request', ''))
        if signed_request:
            kwargs.update({'signed_request': signed_request})

        return func(request, *args, **kwargs)

    return wrapper

@facebook_decorator
def get_friends(request, **kwargs):
    token = kwargs['access_token']
    graph = kwargs['graph']
    user_path = request.user.username + "/friends"
    friends = graph.get(user_path).get('data')
    return friends

@facebook_decorator
def get_fb_groups(request, **kwargs):
    token = kwargs['access_token']
    graph = kwargs['graph']
    user_path = request.user.username + "/groups"
    groups = graph.get(user_path).get('data')
    return groups

#first few functions taken from django_social_auth example at
#https://github.com/omab/django-social-auth/blob/master/example/app/facebook.py
def is_complete_authentication(request):
    return request.user.is_authenticated() and \
        FacebookBackend.__name__ in request.session.get(BACKEND_SESSION_KEY, '')

def get_access_token(user):
    key = str(user.id)
    access_token = cache.get(key)

    # If cache is empty read the database
    if access_token is None:
        try:
            social_user = user.social_user if hasattr(user, 'social_user') \
                else UserSocialAuth.objects.get(user=user.id, 
                                                provider=FacebookBackend.name)
        except UserSocialAuth.DoesNotExist:
            return None

        if social_user.extra_data:
            access_token = social_user.extra_data.get('access_token')
            expires = social_user.extra_data.get('expires')

            cache.set(key, access_token, 
                      int(expires) if expires is not None else 0)

    return access_token

@facebook_decorator
def importgroup(request, group, **kwargs):
    #import a group from Facebook
    def create_ret_user(user_info):
        #if user doesn't exist, create it. Return None if Facebook is
       	#missing information on them; otherwise, return MyUser object
        try:
            result = MyUser.objects.filter(
                username = user_info['username'])
            if len(result) != 0:
                assert(len(result) == 1)
                return result[0]
            new_user = MyUser(username = user_info['username'],
                              first_name = user_info['first_name'],
                              last_name = user_info['last_name'])
        except KeyError:
            return None
        new_user.save()
        return new_user
    print "I am here"
    if request.user.username == "":
        return HttpResponse('Unauthorized access', status=401)
    this_user = MyUser.objects.get(username = request.user.username)	

    token = kwargs['access_token']
    graph = kwargs['graph']

    group_info = graph.get("/" + str(group))
    #check if this group already exists
    db_groups = MyGroup.objects.filter(creator=request.user.username,
                                       name=group_info['name'])
    if len(db_groups) != 0:
        return HttpResponse("Group already exists!", status=401)

    #save group, except for member info
    new_group = MyGroup()
    new_group.name = group_info['name']
    new_group.creator = request.user.username
    new_group.save()
    
    #save member info
    members = graph.get("/" + str(group) + "/members").get('data')
    for member in members:
        fb_user = graph.get("/" + member['id'])
        our_user = create_ret_user(fb_user) #MyUser object
        if our_user != None:
            new_group.users.add(our_user)
    new_group.save()
    return HttpResponseRedirect('/frontend/personal')

def import_events(request):
    # Import event from Facebook
    user = request.user
    instance = UserSocialAuth.objects.get(user=user, provider='facebook')
    token = instance.tokens['access_token']
    graph = GraphAPI(token)
    user_path = str(instance.uid) + "/events"

    fb_events = graph.get(user_path).get('data')

    print "HELLO WORLD"

    print user_path
    print fb_events

    for e in fb_events:
        print e

    return HttpResponseRedirect('/')

def process_export(user, event_obj, token, graph):
    #helper function to export event to Facebook
    #user and event_obj are MyUser and NewEvent type, respectively. Returns
    #True on success, False on failure
    if event_obj.private:
        privacy_type = "SECRET"
    else:
        privacy_type = "OPEN"
    event_path = user.username + "/events"
    event_data = {
        'name' : event_obj.name,
        'start_time' : event_obj.startTime.isoformat(),
        'end_time': event_obj.endTime.isoformat(),
        'location' : event_obj.location,
        'privacy_type' : privacy_type
        }
    result = graph.post(path=event_path, **event_data)
    if result.get('id', False):
        return True
    else:
        return False

@facebook_decorator
def export_event(request, event, **kwargs):
    #export event to Facebook
    try:
        event_obj = NewEvent.objects.get(id = event)
    except ObjectDoesNotExist:
        return HttpResponse('Tried exporting non-existent event!', 
                            status=401)
    this_user = MyUser.objects.get(username = request.user.username)
    if event_obj.creator != this_user:
        return HttpResponse('Unauthorized access', status=401)
    success = process_export(this_user, event_obj, kwargs['access_token'],
                             kwargs['graph'])
    if success:
        event_obj.exported = True
        event_obj.save()
        return HttpResponseRedirect('/frontend/personal')
    return HttpResponse('Export failed!', status=401)


