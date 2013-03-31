from django.conf.urls import patterns, include, url
from frontend import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^$', views.add, name='add')
)
