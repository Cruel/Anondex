from django.conf.urls.defaults import *
from django.views.generic.simple import redirect_to, direct_to_template

urlpatterns = patterns('home.views',
    url(r'^$', redirect_to, {'url': '/'}),
    url(r'^create$', direct_to_template, {'template': 'home/create.html'}, name='create'),
    url(r'^mypage$', direct_to_template, {'template': 'home/mypage.html'}, name='mypage'),
)