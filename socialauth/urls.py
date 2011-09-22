from django.conf.urls.defaults import *

urlpatterns = patterns('socialauth.views',
    url(r'^$', 'home'),
    url(r'^done/$', 'done'),
    url(r'^error/$', 'error'),
    url(r'^logout/$', 'logout'),
    url(r'^email/$', 'email'),
    url(r'^welcome/$', 'welcome', name='newly_registered'),
    url(r'^associate/complete/(?P<backend>[^/]+)/$', 'associate_complete_wrapper'),
    url(r'^username/$', 'username', name='socialauth_username'),
    #url(r'^login/(?P<backend>[^/]+)/$', 'auth_register', name='socialauth_begin'),
    url(r'', include('social_auth.urls')),
)