# Define a custom User class to work with django-social-auth
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import redirect

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """Create a matching profile whenever a user object is created."""
    if created:
        profile, new = Profile.objects.get_or_create(user=instance)

class Profile(models.Model):
    GENDER_CHOICES = (
        (1, 'Male'),
        (2, 'Female'),
    )
    user = models.OneToOneField(User, unique=True)
    #first_name = models.CharField(_('first name'), max_length=100)
    #middle_name = models.CharField(_('middle name'), blank=True, max_length=100)
    #last_name = models.CharField(_('last name'), max_length=100)
    #slug = models.SlugField(_('slug'), unique=True)
    gender = models.PositiveSmallIntegerField(choices=GENDER_CHOICES, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = 'Profiles'
        verbose_name_plural = 'Profiles'
        #ordering = ('last_name', 'first_name',)
    def __unicode__(self):
        return self.user.username


from social_auth.signals import pre_update, socialauth_registered, socialauth_not_registered
from social_auth.backends.facebook import FacebookBackend
from social_auth.models import UserSocialAuth
UserSocial = UserSocialAuth._meta.get_field('user').rel.to

def facebook_extra_values(sender, user, response, details, **kwargs):
    user.gender = response.get('gender')
    return True

def testy1(sender, user, response, details, **kwargs):
    user.is_active = False
    return True

def testy2(sender, uid, response, details, **kwargs):
    print "k2"
    return True

def user_test(sender, response, details, **kwargs):
    name = sender.username(details)
    user = UserSocial.objects.create_user(username=name, email=details['email'])
    user.is_active = False
    kwargs['request'].session['social_auth_new_username'] = details['username']
    return user

pre_update.connect(facebook_extra_values, sender=FacebookBackend)
socialauth_registered.connect(testy1)
socialauth_not_registered.connect(testy2)