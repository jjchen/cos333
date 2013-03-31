from django.conf.urls import patterns, include, url
from frontend import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^/adding/$', views.add, name='add')
)
