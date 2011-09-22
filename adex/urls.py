from django.conf.urls.defaults import *

urlpatterns = patterns('adex.views',
    (r'^$', 'browse'),
    (r'^tagged/(?P<tag>\d+)/$', 'tagged'),
)