from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect

from social_auth import __version__ as version
from django.core.mail import send_mail
from social_auth.views import associate_complete

@login_required
def associate_complete_wrapper(request, backend):
    try:
        return associate_complete(request, backend)
    except ValueError, e:
        if e and len(e.args) > 0:
            if e[0] == 'Account already in use.':
                messages.error(request, "Authentication already used on account: %s" % e[1])
            #for err in e.args:
                #messages.error(request, "Authentication Error: %s" % err)
                #messages.error(request, err)
    return redirect('/auth/')

def email(request):
    send_mail('Subject here', 'Here is the message.', 'no-reply@anondex.com', ['machin3@gmail.com'], fail_silently=False)

def home(request):
    """Home view, displays login mechanism"""
    if request.user.is_authenticated():
        return HttpResponseRedirect('done')
    else:
        return render_to_response('socialauth/home.html', {'version': version},
                                  RequestContext(request))

@login_required
def done(request):
    """Login complete view, displays user data"""
    ctx = {'accounts': request.user.social_auth.all(),
           'version': version,
           'last_login': request.session.get('social_auth_last_login_backend')}
    return render_to_response('socialauth/done.html', ctx, RequestContext(request))

def error(request):
    error_msg = request.session.pop(settings.SOCIAL_AUTH_ERROR_KEY, None)
    return render_to_response('socialauth/error.html', {'version': version,
                                             'error_msg': error_msg},
                              RequestContext(request))

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')
