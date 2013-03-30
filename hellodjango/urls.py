from django.conf.urls import patterns, include, url
#from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^polls/', include('polls.urls')),
                       url(r'^oc/', include('oc.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       url('', include('oc.urls'))
#                       (r'^time/$', current_datetime)
    # Examples:
    # url(r'^$', 'hellodjango.views.home', name='home'),
    # url(r'^hellodjango/', include('hellodjango.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
