from django.conf.urls.defaults import *

urlpatterns = patterns('',    
    url(r'^(?P<content_type>\d+)/(?P<object_id>\d+)/(?P<creator_field>\w+)$', 'reporting.views.flag', name="report"),
)