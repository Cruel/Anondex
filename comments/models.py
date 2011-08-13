from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.contrib.comments.models import Comment
from django.contrib.comments.views import comments
from django.contrib.comments.signals import comment_will_be_posted
from django.dispatch.dispatcher import receiver
from medialibrary.models import LibraryFile


class ImageOld(models.Model):
    EXTENSION_CHOICES = {
        1 : 'image/jpeg',
        2 : 'image/png',
        3 : 'image/gif',
    }
    width = models.IntegerField()
    height = models.IntegerField()
    #ext = models.TextField(blank=True)
    md5 = models.CharField(max_length=60, unique=True)
    rating = models.FloatField(default=0.0)
    rating_total = models.IntegerField(default=0)
    vote_count = models.IntegerField(default=0)
    name = models.CharField(max_length=60)
    def save(self):
        # TODO: make thumbnail here?
        #self.md5 = "test"
        super(ImageOld, self).save()
        pass
    def __unicode__(self):
        return self.name

class AdexComment(Comment):
    #title = models.CharField(max_length=300)
    #image = models.ForeignKey(Image, null=True)
    file = models.ForeignKey(LibraryFile, null=True)

@receiver(comment_will_be_posted, sender=AdexComment)
def my_callback(sender, comment, request, **kwargs):
    print "my_callback"
    #comment.comment = "LOCHANGED2"