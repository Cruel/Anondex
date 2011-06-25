from django.conf.urls.defaults import *

urlpatterns = patterns('comments.views',
    (r'^$', 'index'),
    (r'^(?P<comment_id>\d+)/$', 'detail'),
)