from copy import copy
from datetime import datetime
from genericpath import getsize
import mimetypes
import os
import string
from django.contrib.auth.models import User
from django.core.files.move import file_move_safe
from django.core.files.uploadedfile import UploadedFile
from django.db import models
from tagging.fields import TagField
from tagging.utils import parse_tag_input
from os.path import basename
from PIL import Image as pil
from comments.utils import md5_file
from medialibrary.utils import get_video_size, genVideoThumb, get_media_duration, LIBRARYFILE_THUMB_WIDTH, LIBRARYFILE_THUMB_HEIGHT
import settings

LIBRARYFILE_MAX_FILESIZE = 50000000

class LibraryFile(models.Model):
    MEDIA_CHOICES = (
        (1, 'image'),
        (2, 'video'),
        (3, 'audio'),
        (4, 'flash'),
    )
    IMAGE_EXTENSIONS = ('image/jpeg','image/png','image/gif')
    VIDEO_EXTENSIONS = ('video/webm','video/x-flv','video/mpeg','video/mp4')
    AUDIO_EXTENSIONS = ('audio/mp3','audio/mpeg','audio/midi')
    FLASH_EXTENSIONS = ('application/x-shockwave-flash')
    date        = models.DateTimeField(default=datetime.now)
    user        = models.ForeignKey(User, null=True, blank=True)
    ip          = models.IPAddressField()
    type        = models.PositiveSmallIntegerField(choices=MEDIA_CHOICES)
    width       = models.IntegerField(null=True, blank=True)
    height      = models.IntegerField(null=True, blank=True)
    length      = models.IntegerField(null=True, blank=True)
    filesize    = models.IntegerField()
    md5         = models.CharField(max_length=60, unique=True)
    name        = models.CharField(max_length=60)
    filename    = models.CharField(max_length=60)
    tags        = TagField()

    def get_tag_list(self):
        return parse_tag_input(self.tags)

    def save_image(self, filename):
        self.type = 1
        im = pil.open(filename)
        (self.width, self.height) = im.size
        super(LibraryFile, self).save() # Intermediate save to get new ID
        self.filename = "adex%s_%s" % (self.id, self.name)
        im.thumbnail((LIBRARYFILE_THUMB_WIDTH,LIBRARYFILE_THUMB_HEIGHT), pil.ANTIALIAS)
        im.save(settings.MEDIA_ROOT + "i/thumb/%s" % self.filename)
        file_move_safe(filename, settings.MEDIA_ROOT + "i/%s" % self.filename)

    def save_video(self, filename):
        self.type = 2
        (self.width, self.height) = get_video_size(filename)
        self.length = get_media_duration(filename)
        super(LibraryFile, self).save() # Intermediate save to get new ID
        self.filename = "adex%s_%s" % (self.id, self.name)
        genVideoThumb(filename, settings.MEDIA_ROOT + "v/thumb/%s.jpg" % self.filename)
        file_move_safe(filename, settings.MEDIA_ROOT + "v/%s" % self.filename)

    def save_audio(self, filename):
        self.type = 3
        self.length = get_media_duration(filename)
        super(LibraryFile, self).save() # Intermediate save to get new ID
        self.filename = "adex%s_%s" % (self.id, self.name)
        file_move_safe(filename, settings.MEDIA_ROOT + "a/%s" % self.filename)

    def save_flash(self, filename):
        self.type = 4
        im = pil.open(filename)
        (self.width, self.height) = im.size
        super(LibraryFile, self).save() # Intermediate save to get new ID
        self.filename = "adex%s_%s" % (self.id, self.name)
        im.thumbnail((LIBRARYFILE_THUMB_WIDTH,LIBRARYFILE_THUMB_HEIGHT), pil.ANTIALIAS)
        im.save(settings.MEDIA_ROOT + "i/thumb/%s" % self.filename)
        file_move_safe(filename, settings.MEDIA_ROOT + "i/%s" % self.filename)

    def save_file(self, file):
        if isinstance(file, UploadedFile):
            base, ext = os.path.splitext(file.name)
            filename = base[:40] + ext
            filename = settings.MEDIA_ROOT + 'tmp/' + string.replace(filename, ' ', '_')
            content_type = file.content_type
            destination = open(filename, 'wb+')
            print "Opened %s for writing as %s..." % (filename, content_type)
            for chunk in file.chunks():
                destination.write(chunk)
            destination.close()
            file = filename
        else:
            content_type = mimetypes.guess_type(file)[0]

        self.md5 = md5_file(file)
        try:
            # Get class values from existing file with same md5 (if it exists)
            f = LibraryFile.objects.get(md5=self.md5)
            self.__dict__ = f.__dict__
        except LibraryFile.DoesNotExist:
            self.name = basename(file)
            self.filesize = getsize(file)
            if self.filesize > LIBRARYFILE_MAX_FILESIZE:
                raise Exception, 'File "%s" (%d) is greater than maximum file size of %d' % (self.name, self.filesize, LIBRARYFILE_MAX_FILESIZE)

            if content_type in self.IMAGE_EXTENSIONS:
                self.save_image(file)
            elif content_type in self.VIDEO_EXTENSIONS:
                self.save_video(file)
            elif content_type in self.AUDIO_EXTENSIONS:
                self.save_audio(file)
            elif content_type in self.FLASH_EXTENSIONS:
                self.save_flash(file)
            else:
                raise Exception, 'Not a valid LibraryFile MIME type "%s" for file "%s"' % (content_type, self.name)
            super(LibraryFile, self).save()

    def delete(self):
        if self.type == 1: # Image
            os.remove("%si/thumb/%s" % (settings.MEDIA_ROOT, self.filename))
            os.remove("%si/%s" % (settings.MEDIA_ROOT, self.filename))
        elif self.type == 2: # Video
            os.remove("%sv/thumb/%s.jpg" % (settings.MEDIA_ROOT, self.filename))
            os.remove("%sv/%s" % (settings.MEDIA_ROOT, self.filename))
        elif self.type == 3: # Audio
            os.remove("%sa/%s" % (settings.MEDIA_ROOT, self.filename))
        elif self.type == 4: # Flash
            os.remove("%sf/thumb/%s.jpg" % (settings.MEDIA_ROOT, self.filename))
            os.remove("%sf/%s" % (settings.MEDIA_ROOT, self.filename))
        super(LibraryFile, self).delete()

    def thumbnail_url(self):
        filename = self.filename
        if self.type == 1: folder = 'i'
        elif self.type == 2:
            folder = 'v'
            filename += '.jpg'
        elif self.type == 3: folder = 'a'
        elif self.type == 4: folder = 'f'
        return settings.MEDIA_URL + folder + '/thumb/' + filename

    def thumbnail(self):
        #return u'<img src="%s" />' % (self.thumbnail())
        extra_class = 'height' if self.height >= self.width else 'width'
        if self.type == 2:
            return u'<div class="adexthumb"><div class="%s" style="background-image:url(%s)"></div></div>' % (extra_class, self.thumbnail_url())
        else:
            return u'<div class="adexthumb"><img class="%s" src="%s" /></div>' % (extra_class, self.thumbnail_url())

    def type_name(self):
        return self.MEDIA_CHOICES[self.type-1][1]

    def content_type(self):
        return mimetypes.guess_type(self.filename)[0]
    
    thumbnail.short_description = 'Thumbnail'
    thumbnail.allow_tags = True
    def __unicode__(self):
        return "%s [%s]" % (self.name or self.filename, self.type_name())