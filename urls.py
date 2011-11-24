import os
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from socialauth.forms import ProfileForm, RegistrationFormTest
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
    url(r'^image/(?P<file_id>\d+)$', 'comments.views.image_page', name='image'),
    url(r'^video/(?P<file_id>\d+)$', 'comments.views.video_page', name='video'),
    url(r'^audio/(?P<file_id>\d+)$', 'comments.views.audio_page', name='audio'),
    url(r'^flash/(?P<file_id>\d+)$', 'comments.views.flash_page', name='flash'),

    # Admin
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # Login / Auth
    #url(r'auth/', include('social_auth.urls')),
    url(r'^auth/', include('socialauth.urls')),
    url(r'^login/$', 'socialauth.views.auth_login', name='login'),
    url(r'^logout/$', 'socialauth.views.auth_logout', name='logout'),
    url(r'^account/register/$', 'registration.views.register',
         {'form_class': RegistrationFormTest}, 'registration_register'),
    url(r'^account/', include('registration.urls')),

    #(r'^profiles/edit/', 'profiles.views.edit_profile', {'form_class': ProfileForm,'success_url':'/my/custom/url',}),
    url(r'^user/(?P<username>\w+)/$', 'home.views.profile', name='profiles_profile_detail'),
    #url(r'^user/', include('profiles.urls')),
    url(r'^profile/edit/', 'profiles.views.edit_profile', {'form_class': ProfileForm,}, name='profiles_edit_profile'),

    # Misc
    url(r'^upload_image$', 'comments.views.upload_image'),
    url(r'^upload_file$', 'adex.views.upload_file'),
    url(r'^ajax/', include('home.ajax_urls')),
    url(r'^lib/', include('medialibrary.urls')),
    url(r'^login_redirect/$', direct_to_template, {'template': 'socialauth/login_redirect.html'}),
    url(r'^auth_redirect/$', direct_to_template, {'template': 'socialauth/auth_redirect.html'}),
    url(r'^flashview/', 'comments.views.flashview'),

    url(r'^vid/$', 'adex.views.test_video'),

    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',  {'document_root': settings.ROOT_PATH+'/_generated_media/', 'show_indexes': True}),
)