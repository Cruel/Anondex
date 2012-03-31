from django.conf.urls.defaults import *

urlpatterns = patterns('reporting.views',
    url(r'^(?P<content_type>\d+)/(?P<object_id>\d+)/(?P<creator_field>\w+)$', 'flag', name="report"),
)