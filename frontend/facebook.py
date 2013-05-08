from social_auth.models import UserSocialAuth
from facepy import GraphAPI
from frontend.models import MyUser
from frontend.models import MyGroup
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from frontend.models import NewEvent

def importgroup(request, group):
    #import a group from Facebook
    def create_ret_user(user_info):
        #if user doesn't exist, create it. Return None if Facebook is
       	#missing information on them; otherwise, return MyUser object
        try:
            result = MyUser.objects.filter(
                user_id = user_info['username'])
            if len(result) != 0:
                assert(len(result) == 1)
                return result[0]
            new_user = MyUser(user_id = user_info['username'],
                              first_name = user_info['first_name'],
                              last_name = user_info['last_name'])
        except KeyError:
            return None
        new_user.save()
        return new_user

    if request.user.username == "":
        return HttpResponse('Unauthorized access', status=401)
    this_user = MyUser.objects.get(user_id = request.user.username)	
    instance = UserSocialAuth.objects.get(user=this_user, provider='facebook')        
    token = instance.tokens['access_token']
    graph = GraphAPI(token)	

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

def process_export(user, event_obj):
    #helper function to export event to Facebook
    #user and event_obj are MyUser and NewEvent type, respectively. Returns
    #True on success, False on failure
    instance = UserSocialAuth.objects.get(user=user, provider='facebook')       
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
    result = graph.post(path=event_path, **event_data)
    if result.get('id', False):
        return True
    else:
        return False

def exportevent(request, event):
    #export event to Facebook
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
        event_obj.exported = True
        event_obj.save()
        return HttpResponseRedirect('/frontend/personal')
    return HttpResponse('Export failed!', status=401)

def get_fb_groups(user):
    instance = UserSocialAuth.objects.get(user=user, provider='facebook') 
    token = instance.tokens['access_token']
    graph = GraphAPI(token)

    print "Facebook instance: " + str(instance)

    user_path = str(instance.uid) + "/groups"
    groups = graph.get(user_path).get('data')
    return groups

def get_friends(user):
    instance = UserSocialAuth.objects.get(user=user, provider='facebook')
    token = instance.tokens['access_token']
    graph = GraphAPI(token)
    user_path = str(instance.uid) + "/friends"
    friends = graph.get(user_path).get('data')

    return friends




