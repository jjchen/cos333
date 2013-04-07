from django.shortcuts import render_to_response
# Create your views here.
def index(request):
    print request.user
    print vars(request.user)
    #print request.user.first_name
    return render_to_response('frontend/map.html')
