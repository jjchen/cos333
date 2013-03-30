from django.conf.urls import patterns, include, url
from timeline import views

urlpatterns = patterns('',
    # ex: /polls/
    url(r'^$', views.index, name='index')
)



