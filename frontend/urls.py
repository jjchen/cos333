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
    url(r'^refresh/', views.refreshEvents, name='refresh_events'),
    url(r'^rsvp/(?P<event>\w+)/', views.addrsvp, name='addrsvp'),
    url(r'^rmrsvp/(?P<event>\w+)/', views.rmrsvp, name='rmrsvp'),
    url(r'^rmgroup/(?P<group>\w+)/$', views.rmgroup, name='rmgroup'),
    url(r'^tagging_autocomplete_tagit/', include('tagging_autocomplete_tagit.urls')),
    url(r'^rmfriend/(?P<user>\w+)/$', views.rmfriend, name='rmfriend'),
)
