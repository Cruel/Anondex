from django.conf.urls.defaults import *
from anondex.socialauth.forms import ProfileForm, RegistrationFormTest
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Initialize comments ajax wrapper
from comments import ajax_wrapper

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'home.views.index', name='home'),
    url(r'^browse/(?P<page>\d+)$', 'home.views.browse', name='browse'),
    url(r'^home/', include('home.urls')),
    url(r'^poll/', include('polls.urls')),
    url(r'^comment/', include('django.contrib.comments.urls')),
    url(r'^comments/', include('comments.urls')),
    url(r'^image/(?P<image_id>\d+)$', 'comments.views.image_page'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    #url(r'auth/', include('social_auth.urls')),
    url(r'^auth/', include('socialauth.urls')),
    url(r'^user/register/$', 'registration.views.register',
         {'backend': 'registration.backends.default.DefaultBackend', 'form_class': RegistrationFormTest}, 'registration_register'),
    url(r'^user/', include('registration.backends.default.urls')),
    url(r'^profiles/edit/', 'profiles.views.edit_profile', {'form_class': ProfileForm,}),
    #(r'^profiles/edit/', 'profiles.views.edit_profile', {'form_class': ProfileForm,'success_url':'/my/custom/url',}),
    url(r'^profiles/', include('profiles.urls')),
    url(r'^upload_image?.*$', 'comments.views.upload_image'),
    url(r'^get_upload_progress?.*$', 'comments.views.get_upload_progress'),
    url(r'^ajax/', include('home.ajax_urls')),

    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',  {'document_root': settings.STATIC_ROOT, 'show_indexes': True}),
)

#urlpatterns += staticfiles_urlpatterns()