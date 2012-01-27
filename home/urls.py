from django.conf.urls.defaults import *
from django.views.generic.simple import redirect_to, direct_to_template

urlpatterns = patterns('home.views',
#    url(r'^$', redirect_to, {'url': '/'}),
    url(r'^create$', direct_to_template, {'template': 'home/create.html'}, name='home_create'),
    url(r'^upload$', direct_to_template, {'template': 'home/create.html'}, name='home_upload'),
    url(r'^privacy$', direct_to_template, {'template': 'home/privacypolicy.html'}, name='home_privacy'),
    url(r'^tos$', direct_to_template, {'template': 'home/tos.html'}, name='home_tos'),
    url(r'^about$', direct_to_template, {'template': 'home/about.html'}, name='home_about'),
)