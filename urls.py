from django.conf.urls.defaults import *
from anondex.socialauth.forms import ProfileForm, RegistrationFormTest
#from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'anondex.home.views.index'),
    (r'^poll/', include('polls.urls')),
    (r'^comment/', include('comments.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    #(r'auth/', include('social_auth.urls')),
    (r'^auth/', include('socialauth.urls')),
    (r'^accounts/register/$', 'registration.views.register',
         {'backend': 'registration.backends.default.DefaultBackend', 'form_class': RegistrationFormTest}, 'registration_register'),
    (r'^acc/', include('registration.backends.default.urls')),
    (r'^profiles/edit/', 'profiles.views.edit_profile', {'form_class': ProfileForm,}),
    #(r'^profiles/edit/', 'profiles.views.edit_profile', {'form_class': ProfileForm,'success_url':'/my/custom/url',}),
    (r'^profiles/', include('profiles.urls')),
)

#urlpatterns += staticfiles_urlpatterns()