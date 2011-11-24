from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.utils import IntegrityError
from django.http import HttpResponseRedirect
from django.contrib.auth import logout, login, authenticate, REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt

from social_auth import __version__ as version
from django.core.mail import send_mail
from social_auth.backends.pipeline.social import social_auth_user
from social_auth.models import UserSocialAuth
from social_auth.views import associate_complete, auth, dsa_view, auth_complete, SESSION_EXPIRATION, SOCIAL_AUTH_LAST_LOGIN, NEW_USER_REDIRECT, DEFAULT_REDIRECT, LOGIN_ERROR_URL
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

#def username(request):
#    name = request.session.get('social_auth_new_username')
#    ctx = {'username': name}
#    if name is not None:
#        if request.method == 'POST':
#            new_name = request.POST['username']
#            try:
#                User.objects.filter(username=name).update(username=new_name, is_active=True)
#            except IntegrityError:
#                ctx['duplicate_name'] = new_name
#                return render_to_response('socialauth/username.html', ctx, RequestContext(request))
#            del request.session['social_auth_new_username']
#            return redirect(request.session.get('social_auth_referer'))
#        else:
#            return render_to_response('socialauth/username.html', ctx, RequestContext(request))
#    else:
#        return redirect('/auth/')

@csrf_exempt
@dsa_view()
def complete(request, backend, *args, **kwargs):
    backend_name = backend.AUTH_BACKEND.name
    new_username = request.session.get(backend_name)

    if new_username:
        user = User.objects.get(username=new_username)
    else:
        user = auth_complete(request, backend, *args, **kwargs)

    if not user.is_active:
        request.session[backend_name] = user.username
        username = request.POST.get('username')
        if username:
            user.username = username
            user.is_active = True
            user.save()
            del request.session[backend_name]
            return redirect(reverse('socialauth_begin', args=[backend_name]))
        else:
            return render_to_response('socialauth/username.html', {'username':user.username}, RequestContext(request))
    return complete_process(request, backend, user=user, *args, **kwargs)

# From social_auth/views.py
def complete_process(request, backend, user, *args, **kwargs):
    """Authentication complete process"""
    #user = auth_complete(request, backend, *args, **kwargs)

    if user and getattr(user, 'is_active', True):
        login(request, user)
        # user.social_user is the used UserSocialAuth instance defined
        # in authenticate process
        social_user = user.social_user

        if SESSION_EXPIRATION :
            # Set session expiration date if present and not disabled by
            # setting. Use last social-auth instance for current provider,
            # users can associate several accounts with a same provider.
            if social_user.expiration_delta():
                request.session.set_expiry(social_user.expiration_delta())

        # store last login backend name in session
        request.session[SOCIAL_AUTH_LAST_LOGIN] = social_user.provider

        # Remove possible redirect URL from session, if this is a new account,
        # send him to the new-users-page if defined.
        url = NEW_USER_REDIRECT if NEW_USER_REDIRECT and \
                                   getattr(user, 'is_new', False) else \
              request.session.pop(REDIRECT_FIELD_NAME, '') or \
              DEFAULT_REDIRECT
    else:
        url = LOGIN_ERROR_URL
    return HttpResponseRedirect(url)

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

from django.contrib.auth.views import login as login_view
def auth_login(request):
    if request.user.is_authenticated():
        redirect_url = request.GET.get('next') or LOGIN_REDIRECT_URL
        return redirect(redirect_url)
    else:
        return login_view(request)
        #return render_to_response('registration/login.html', {}, RequestContext(request))

def auth_logout(request):
    logout(request)
    return redirect('/')
