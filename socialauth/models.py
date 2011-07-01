# Define a custom User class to work with django-social-auth
from django.db import models
from django.contrib.auth.models import User
#from profiles import views as profile_views
#from socialauth.forms import ProfileForm

from django.db.models.signals import post_save
from django.dispatch import receiver

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


from social_auth.signals import pre_update
from social_auth.backends.facebook import FacebookBackend

def facebook_extra_values(sender, user, response, details, **kwargs):
    return False

pre_update.connect(facebook_extra_values, sender=FacebookBackend)
