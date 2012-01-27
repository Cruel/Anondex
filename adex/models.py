from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from djangoratings.fields import AnonymousRatingField
from tagging.fields import TagField
from tagging.models import Tag
from medialibrary.models import LibraryFile
import simplejson as json
from medialibrary.utils import LIBRARYFILE_THUMB_WIDTH, LIBRARYFILE_THUMB_RATIO
import settings

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
        (2, 'Flash'),
        (3, 'URL'),
        (4, 'HTML'),
    )
    item_code       = models.CharField(max_length=5, unique=True)
    domain          = models.CharField(max_length=40, null=True, blank=True)
    title           = models.CharField(max_length=90)
    description     = models.TextField()
    date            = models.DateTimeField(default=datetime.now)
    user            = models.ForeignKey(User, null=True, blank=True)
    ip              = models.IPAddressField()
    content_rating  = models.PositiveSmallIntegerField(choices=CONTENT_RATING, default=0)
    status          = models.PositiveSmallIntegerField(choices=STATUS, default=0)
    type            = models.PositiveSmallIntegerField(choices=CONTENT_TYPE)
    rating          = AnonymousRatingField(range=5)
    media           = models.ManyToManyField(LibraryFile)
    data            = models.TextField()
    tags            = TagField()

    expiration      = models.IntegerField(null=True)
    dead            = models.BooleanField(default=False)
    redeemval       = models.IntegerField(default=0)

    def thumbnail(self, width=LIBRARYFILE_THUMB_WIDTH):
        data = json.loads(self.data)
        if self.type == 0:
            media_id = data['image']['id']
        elif self.type == 1:
            media_id = data['video']['id']
        elif self.type == 2:
            media_id = data['flash']['id']
        elif self.type >= 3:
            height = width / LIBRARYFILE_THUMB_RATIO
            return u'<span class="webkit-scrollbars"><div class="adexthumb webthumb" style="width:%dpx;height:%dpx;"><img style="width:%dpx;" src="%s" /></div></span>' %\
                   (width, height, width, settings.MEDIA_URL+'webthumb/%d.jpg'%self.id)
        try:
            file = LibraryFile.objects.get(pk=media_id)
            return file.thumbnail(width)
        except LibraryFile.DoesNotExist:
            return 'Error'

    def thumbnail_url(self):
        data = json.loads(self.data)
        if self.type == 0:
            media_id = data['image']['id']
        elif self.type == 1:
            media_id = data['video']['id']
        elif self.type == 2:
            media_id = data['flash']['id']
        elif self.type >= 3:
            return settings.MEDIA_URL+'webthumb/%d.jpg' % self.id
        try:
            file = LibraryFile.objects.get(pk=media_id)
            return file.thumbnail_url()
        except LibraryFile.DoesNotExist:
            return 'Error'
        
    def template(self):
        if self.type == 0:
            return 'adex/image.html'
        elif self.type == 1:
            return 'adex/video.html'
        elif self.type == 2:
            return 'adex/flash.html'
        elif self.type == 3:
            return 'adex/url.html'
        else:
            return 'adex/image.html'

    def url(self):
        #return '/?%s' % self.item_code
        return reverse('adex_details', args=[self.pk])
        
    def __unicode__(self):
        return self.title


#class AdexTempInfo(models.Model):
#    adex = models.ForeignKey(Adex)
#    expiration = models.IntegerField()
#    dead = models.IntegerField()
#    redeemval = models.IntegerField()
#    def __unicode__(self):
#        return self.adex.title
