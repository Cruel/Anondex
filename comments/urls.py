from django.conf.urls.defaults import *

urlpatterns = patterns('comments.views',
    (r'^$', 'index'),
    (r'^(?P<item_id>\d+)/$', 'detail'),
)