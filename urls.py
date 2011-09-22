import os
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from anondex.socialauth.forms import ProfileForm, RegistrationFormTest
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

#from django import template
#template.add_to_builtins('project.app.templatetags.custom_tag_module')

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    # Home
    url(r'^$', 'home.views.index', name='home'),

    url(r'^home/', include('home.urls')),
    url(r'^browse/(?P<page>\d+)$', 'home.views.browse', name='browse'),

    # Adex
    url(r'^create$', 'adex.views.create_adex'),
    url(r'^preview$', 'adex.views.preview'),

    # Comments
    url(r'^comment/', include('django.contrib.comments.urls')),
    url(r'^comments/', include('comments.urls')),
    url(r'^image/(?P<image_id>\d+)$', 'comments.views.image_page'),

    # Admin
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # Login / Auth
    #url(r'auth/', include('social_auth.urls')),
    url(r'^auth/', include('socialauth.urls')),
    url(r'^login/$', 'socialauth.views.login', name='auth_login'),
    url(r'^account/register/$', 'registration.views.register',
         {'backend': 'registration.backends.default.DefaultBackend', 'form_class': RegistrationFormTest}, 'registration_register'),
    url(r'^account/', include('registration.urls')),

    url(r'^profiles/edit/', 'profiles.views.edit_profile', {'form_class': ProfileForm,}),
    #(r'^profiles/edit/', 'profiles.views.edit_profile', {'form_class': ProfileForm,'success_url':'/my/custom/url',}),
    url(r'^user/', include('profiles.urls')),

    # Misc
    url(r'^upload_image$', 'comments.views.upload_image'),
    url(r'^upload_file$', 'adex.views.upload_file'),
    url(r'^ajax/', include('home.ajax_urls')),
    url(r'^lib/', include('medialibrary.urls')),
    url(r'^login_redirect/$', direct_to_template, {'template': 'socialauth/login_redirect.html'}),

    url(r'^vid/$', 'adex.views.test_video'),

    #url(r'^static/(?P<path>.*)$', 'django.views.static.serve',  {'document_root': settings.STATIC_ROOT, 'show_indexes': True}),
)