from urllib2 import urlopen, HTTPError
from django.core.files.base import ContentFile
from django.template.defaultfilters import slugify
from social_auth.backends.facebook import FacebookBackend
from social_auth.backends import google
from social_auth.backends.twitter import TwitterBackend
from social_auth.signals import pre_update
from socialauth.models import Profile
import urlparse, os

def social_extra_values(sender, user, response, details, **kwargs):
    result = False
    
    if "id" in response:
        try:
            url = None
            if sender == FacebookBackend:
                url = "http://graph.facebook.com/%s/picture?type=large" % response["id"]
            elif sender == google.GoogleOAuth2Backend and "picture" in response:
                url = response["picture"]
            elif sender == TwitterBackend:
                url = response["profile_image_url"]

            if url:
                avatar = urlopen(url)

                path = urlparse.urlparse(url).path
                ext = os.path.splitext(path)[1]
                profile = Profile.objects.get(user=user)
                profile.avatar.save(
                    slugify(user.username + " social") + '.jpg',
                    ContentFile(avatar.read()),
                    save=False,
                )
                profile.save()

        except HTTPError:
            pass
        
        result = True

    return result

pre_update.connect(social_extra_values, sender=None)

from social_auth.backends import google

google.GOOGLEAPIS_EMAIL = "https://www.googleapis.com/oauth2/v1/userinfo"

def googleapis_email(url, params):
    """A bit of hacking"""
    from urllib2 import Request, urlopen
    from django.utils import simplejson

    request = Request(url + '?' + params, headers={'Authorization': params})
    try:
        return simplejson.loads(urlopen(request).read())
    except (ValueError, KeyError, IOError):
        return None

google.googleapis_email = googleapis_email