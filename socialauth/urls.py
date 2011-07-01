from django.conf.urls.defaults import *

urlpatterns = patterns('socialauth.views',
    url(r'^$', 'home'),
    url(r'^done/$', 'done'),
    url(r'^error/$', 'error'),
    url(r'^logout/$', 'logout'),
    url(r'^email/$', 'email'),
    url(r'^associate/complete/(?P<backend>[^/]+)/$', 'associate_complete_wrapper'),
    url(r'', include('social_auth.urls')),

)