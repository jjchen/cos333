from django.conf.urls import patterns, include, url
from frontend import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),

    url(r'^signup/', views.signup),
    url(r'^settings/', views.settings, name='settings'),
    url(r'', include('social_auth.urls')),

    url(r'^add/$', views.add, name='add'),
    url(r'^addgroup/', views.addgroup, name='addgroup'),
    url(r'^(?P<group>\w+)/$', views.rmgroup, name='rmgroup'),
    url(r'^search/$', views.search, name='search')
)
