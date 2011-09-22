from django.conf.urls.defaults import *
from django.views.generic.simple import redirect_to, direct_to_template

urlpatterns = patterns('home.ajax_views',
    url(r'^$', redirect_to, {'url': '/'}),
    url(r'^taglist$', 'taglist'),
    url(r'^sidebar$', 'sidebar'),
    url(r'^filelist$', 'filelist'),
    url(r'^mypage$', direct_to_template, {'template': 'home/mypage.html'}, name='mypage'),
)