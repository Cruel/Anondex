from django.conf.urls.defaults import *
#from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'comments.views.index'),
    (r'^poll/', include('polls.urls')),
    (r'^comment/', include('comments.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    #(r'auth/', include('social_auth.urls')),
    (r'app/', include('app.urls')),
)

#urlpatterns += staticfiles_urlpatterns()