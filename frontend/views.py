from django.shortcuts import render
# Create your views here.
def index(request):
    context = {'events_list': events_list}
    return render(request, 'frontend/map.html', context)
