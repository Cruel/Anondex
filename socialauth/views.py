from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.utils import IntegrityError
from django.http import HttpResponseRedirect
from django.contrib.auth import logout as auth_logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect

from social_auth import __version__ as version
from django.core.mail import send_mail
from social_auth.models import UserSocialAuth
from social_auth.views import associate_complete, auth
from local_settings import SOCIAL_AUTH_DEFAULT_USERNAME, LOGIN_REDIRECT_URL

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

def username(request):
    name = request.session.get('social_auth_new_username')
    ctx = {'username': name}
    if name is not None:
        if request.method == 'POST':
            new_name = request.POST['username']
            try:
                User.objects.filter(username=name).update(username=new_name, is_active=True)
            except IntegrityError:
                ctx['duplicate_name'] = new_name
                return render_to_response('socialauth/username.html', ctx, RequestContext(request))
            del request.session['social_auth_new_username']
            return redirect(request.session.get('social_auth_referer'))
        else:
            return render_to_response('socialauth/username.html', ctx, RequestContext(request))
    else:
        return redirect('/auth/')

def home(request):
    """Home view, displays login mechanism"""
    if request.user.is_authenticated():
        return HttpResponseRedirect('done')
    else:
        return render_to_response('socialauth/home.html', {'version': version}, RequestContext(request))

def welcome(request):
    """Home view, displays login mechanism"""
    if request.user.is_authenticated():
        return HttpResponseRedirect('done')
    else:
        return render_to_response('socialauth/home.html', {'version': version}, RequestContext(request))

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

def auth_register(request, backend):
    request.session['new_username'] = request.POST['username'] or SOCIAL_AUTH_DEFAULT_USERNAME
    return auth(request, backend)

from django.contrib.auth.views import login as auth_login
def login(request):
    if request.user.is_authenticated():
        redirect_url = request.GET.get('next') or LOGIN_REDIRECT_URL
        return redirect(redirect_url)
    else:
        return auth_login(request)
        #return render_to_response('registration/login.html', {}, RequestContext(request))

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')
