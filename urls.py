from django.conf.urls.defaults import *
from anondex.socialauth.forms import ProfileForm, RegistrationFormTest
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'anondex.home.views.index'),
    (r'^poll/', include('polls.urls')),
    (r'^comments/', include('django.contrib.comments.urls')),
    #(r'^comments/', include('comments.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    #(r'auth/', include('social_auth.urls')),
    (r'^auth/', include('socialauth.urls')),
    (r'^user/register/$', 'registration.views.register',
         {'backend': 'registration.backends.default.DefaultBackend', 'form_class': RegistrationFormTest}, 'registration_register'),
    (r'^user/', include('registration.backends.default.urls')),
    (r'^profiles/edit/', 'profiles.views.edit_profile', {'form_class': ProfileForm,}),
    #(r'^profiles/edit/', 'profiles.views.edit_profile', {'form_class': ProfileForm,'success_url':'/my/custom/url',}),
    (r'^profiles/', include('profiles.urls')),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',  {'document_root': settings.STATIC_ROOT, 'show_indexes': True}),
)

#urlpatterns += staticfiles_urlpatterns()