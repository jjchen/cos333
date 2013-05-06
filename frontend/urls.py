from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from frontend import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),

    url(r'^signup/', views.signup),
    url(r'^settings/', views.settings, name='settings'),
    url(r'', include('social_auth.urls')),

    url(r'^add/', views.add, name='add'),
    url(r'^addgroup/', views.addgroup, name='addgroup'),
    url(r'^addfriend/', views.addfriend, name='addfriend'),
    url(r'^personal/$', views.personal, name='personal'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^search/$', views.search, name='search'),
    url(r'^success/$', TemplateView.as_view(template_name="frontend/success.html"), name="event_success"),
    url(r'^cal/$', views.calendar, name="calendar"),
    url(r'^eventsXML$', views.eventsXML),
    url(r'dataprocessor$', views.dataprocessor),
    url(r'^refresh/', views.refresh, name='refresh'),
    url(r'^rsvp/', views.addrsvp, name='addrsvp'),
    url(r'^rmrsvp/(?P<id>\w+)/', views.rmrsvp, name='rmrsvp'),
    url(r'^rmrsvp/', views.rmrsvp, name='rmrsvp'),
    url(r'^rmgroup/(?P<group>\w+)/$', views.rmgroup, name='rmgroup'),
    url(r'^importgroup/(?P<group>\w+)/$', views.importgroup, 
        name='importgroup'),
    url(r'^rmfriend/(?P<user>\w+)/$', views.rmfriend, name='rmfriend'),
 #   url(r'^tagging_autocomplete_tagit/', include('tagging_autocomplete_tagit.urls')),
    url(r'^rmevent/(?P<event>\w+)/$', views.rmevent, name='rmevent'),
    url(r'^edit/(?P<event>\w+)/$', views.edit, name='edit'),
    url(r'^exportevent/(?P<event>\w+)/$', views.exportevent, 
        name='exportevent'),
    url(r'^personal_ajax/(?P<event>\w+)/$', views.personal_ajax, name='personal_ajax'),
    url(r'^editevent/(?P<event>\w+)/$', views.editevent, name='editevent'),
    url(r'^filter/(?P<tag>\w+)/$', views.filter, name='filter'),
    url(r'^filter/$', views.filter, name='filter_init'),
    url(r'^api/get_names/', views.get_names, name='get_names'),
    url(r'^api/get_tags/', views.get_tags, name='get_tags'),
    url(r'^api/get_memnames/', views.get_memnames, name='get_memnames'),
)

