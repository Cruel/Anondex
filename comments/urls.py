from django.conf.urls.defaults import *

urlpatterns = patterns('comments.views',
    url(r'^(?P<item_id>\d+)/$', 'detail', name='adex_details'),
)