from django.conf.urls.defaults import *

urlpatterns = patterns('app.views',
    url(r'^$', 'home'),
    url(r'^done/$', 'done'),
    url(r'^error/$', 'error'),
    url(r'^logout/$', 'logout'),
    url(r'^email/$', 'email'),
    url(r'', include('social_auth.urls')),

)