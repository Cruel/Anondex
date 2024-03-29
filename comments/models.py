from django.db import models
from django.contrib.comments.models import Comment
from django.contrib.comments.signals import comment_will_be_posted
from django.dispatch.dispatcher import receiver
from djangoratings.fields import AnonymousRatingField, RatingField, RatingManager
from medialibrary.models import LibraryFile


#class ImageOld(models.Model):
#    EXTENSION_CHOICES = {
#        1 : 'image/jpeg',
#        2 : 'image/png',
#        3 : 'image/gif',
#    }
#    width           = models.IntegerField()
#    height          = models.IntegerField()
#    #ext            = models.TextField(blank=True)
#    md5             = models.CharField(max_length=60, unique=True)
#    rating          = models.FloatField(default=0.0)
#    rating_total    = models.IntegerField(default=0)
#    vote_count      = models.IntegerField(default=0)
#    name            = models.CharField(max_length=60)
#    user            = models.ForeignKey(User, blank=True, null=True)
#    submit_date     = models.DateTimeField(_('date/time submitted'), default=None)
#    ip_address      = models.IPAddressField(_('IP address'), blank=True, null=True)
#    def save(self):
#        # TODO: make thumbnail here?
#        #self.md5 = "test"
#        super(ImageOld, self).save()
#        pass
#    def __unicode__(self):
#        return self.name

class AdexComment(Comment):
    is_anonymous = models.BooleanField(u'is anonymous',
                help_text=u'This marks an anonymous post, even with it being linked to a user.')
    file = models.ForeignKey(LibraryFile, null=True, blank=True)
    rating = RatingField(range=2, can_change_vote=True, allow_delete=True)

@receiver(comment_will_be_posted, sender=AdexComment)
def my_callback(sender, comment, request, **kwargs):
    print "my_callback"
    #comment.comment = "LOCHANGED2"

# Initialize comments ajax wrapper
from comments import ajax_wrapper