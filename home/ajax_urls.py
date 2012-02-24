from django.conf.urls.defaults import *
from django.views.generic.simple import redirect_to, direct_to_template
from hitcount.views import update_hit_count_ajax

urlpatterns = patterns('home.ajax_views',
    url(r'^$', redirect_to, {'url': '/'}),
    url(r'^taglist$', 'taglist'),
    url(r'^sidebar$', 'sidebar'),
    url(r'^comment/(?P<comment_id>\d+)$', 'comment'),
#    url(r'^addlibfile/(?P<media_id>\d+)$', 'addlibfile'),
    url(r'^filelist$', 'filelist'),
    url(r'^rate$', 'rate'),
    url(r'^encode_progress', 'encode_progress'),
    #url(r'^report/(?P<type>\w+)/(?P<id>\d+)$', 'report', name='report'),
    url(r'^hit/$', update_hit_count_ajax, name='hitcount_update_ajax'), # keep this name the same

    url(r'^mypage$', direct_to_template, {'template': 'home/mypage.html'}, name='mypage'),
)