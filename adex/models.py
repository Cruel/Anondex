from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from djangoratings.fields import AnonymousRatingField
from tagging.fields import TagField
from tagging.models import Tag
from medialibrary.models import LibraryFile
import simplejson as json

class Adex(models.Model):
    CONTENT_RATING = (
        (0, 'PG'),
        (1, 'PG-13'),
        (2, 'R'),
    )
    STATUS = (
        (0, 'Pending'),
        (1, 'Approved'),
        (2, 'Unapproved'),
        (3, 'Temporary'),
    )
    CONTENT_TYPE = (
        (0, 'Image'),
        (1, 'Video'),
    )
    item_code       = models.CharField(max_length=12, unique=True)
    domain          = models.CharField(max_length=90, null=True, blank=True)
    title           = models.CharField(max_length=90)
    description     = models.TextField()
    date            = models.DateTimeField(default=datetime.now)
    user            = models.ForeignKey(User, null=True, blank=True)
    ip              = models.IPAddressField()
    views           = models.IntegerField(default=0)
    content_rating  = models.PositiveSmallIntegerField(choices=CONTENT_RATING, default=0)
    status          = models.PositiveSmallIntegerField(choices=STATUS, default=0)
    type            = models.PositiveSmallIntegerField(choices=CONTENT_TYPE)
    rating          = AnonymousRatingField(range=5)
    media           = models.ManyToManyField(LibraryFile)
    data            = models.TextField()
    tags            = TagField()
    def thumbnail(self):
        data = json.loads(self.data)
        if self.type == 0:
            media_id = data['image']['id']
                #if x.type == 1:
                    #return x.thumbnail()
        elif self.type == 1:
            media_id = data['video']['id']
        try:
            file = LibraryFile.objects.get(pk=media_id)
            return file.thumbnail()
        except LibraryFile.DoesNotExist:
            return 'Error'
        
    def __unicode__(self):
        return self.title


class AdexTempInfo(models.Model):
    adex = models.ForeignKey(Adex)
    expiration = models.IntegerField()
    dead = models.IntegerField()
    redeemval = models.IntegerField()
    def __unicode__(self):
        return self.adex.title
