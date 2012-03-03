from copy import copy
from datetime import datetime
from genericpath import getsize
import mimetypes
import os
import re
import string
from django.contrib.auth.models import User
from django.core.files.move import file_move_safe
from django.core.files.uploadedfile import UploadedFile
from django.core.urlresolvers import reverse
from django.db import models
from tagging.fields import TagField
from tagging.utils import parse_tag_input
from os.path import basename
import Image as pil
import time
from comments.utils import md5_file
from medialibrary.utils import get_video_size, genVideoThumb, get_media_duration, LIBRARYFILE_THUMB_WIDTH, LIBRARYFILE_THUMB_HEIGHT, THUMB_FRAME_COUNT, LIBRARYFILE_THUMB_RATIO, webthumb, encodeVideo
import settings
from django.template.defaultfilters import slugify

mimetypes.add_type('video/webm','.webm')

LIBRARYFILE_MAX_FILESIZE = 50000000

class LibraryFile(models.Model):
    MEDIA_CHOICES = (
        (1, 'image'),
        (2, 'video'),
        (3, 'audio'),
        (4, 'flash'),
        (5, 'album'),
    )
    # Also see upload.js constants
    IMAGE_EXTENSIONS = r'^image\/(gif|jpeg|png)$'
    VIDEO_EXTENSIONS = r'^video\/'
    AUDIO_EXTENSIONS = r'^audio\/(mp3|mpeg|ogg|midi)$'
    FLASH_EXTENSIONS = r'^application\/x-shockwave-flash$'
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
    related     = models.ManyToManyField("self", blank=True)
    visible     = models.BooleanField(default=True)

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
        file_ext = os.path.splitext(filename)[1]
        new_filename = string.replace(filename, self.name, "%d.mp4" % time.time())
        encodeVideo(filename, new_filename, self.ip)
        (self.width, self.height) = get_video_size(new_filename)
        self.length = get_media_duration(new_filename)
        super(LibraryFile, self).save() # Intermediate save to get new ID
        self.filename = "adex%s_%s" % (self.id, string.replace(self.name, file_ext, '.mp4'))
        genVideoThumb(new_filename, settings.MEDIA_ROOT + "v/thumb/%s.jpg" % self.filename)
        file_move_safe(new_filename, settings.MEDIA_ROOT + "v/%s" % self.filename)


    def save_audio(self, filename):
        self.type = 3
        self.length = get_media_duration(filename)
        super(LibraryFile, self).save() # Intermediate save to get new ID
        self.filename = "adex%s_%s" % (self.id, self.name)
        file_move_safe(filename, settings.MEDIA_ROOT + "a/%s" % self.filename)

    def save_flash(self, filename):
        self.type = 4
        super(LibraryFile, self).save() # Intermediate save to get new ID
        self.filename = "adex%s_%s" % (self.id, self.name)
        webthumb(
            'http://anondex.com/flashview/?'+settings.MEDIA_URL+'tmp/'+self.name,
            settings.MEDIA_ROOT+"f/thumb/%s.jpg"%self.filename,
            is_flash=True,
        )
        file_move_safe(filename, settings.MEDIA_ROOT + "f/%s" % self.filename)
        if settings.DEBUG:
            return



    def save_file(self, file):
        if isinstance(file, UploadedFile):
            base, ext = os.path.splitext(file.name)
            filename = settings.MEDIA_ROOT + 'tmp/' + slugify(base[:40]) + ext
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

            if re.match(self.IMAGE_EXTENSIONS, content_type):
                self.save_image(file)
            elif re.match(self.VIDEO_EXTENSIONS, content_type):
                self.save_video(file)
            elif re.match(self.AUDIO_EXTENSIONS, content_type):
                self.save_audio(file)
            elif re.match(self.FLASH_EXTENSIONS, content_type):
                self.save_flash(file)
            else:
                raise Exception, 'Not a valid LibraryFile MIME type "%s" for file "%s"' % (content_type, self.name)
            super(LibraryFile, self).save()

    def delete(self):
        def delfile(filepath):
            if os.path.isfile(filepath):
                os.remove(filepath)
        if self.type == 1: # Image
            delfile("%si/thumb/%s" % (settings.MEDIA_ROOT, self.filename))
            delfile("%si/%s" % (settings.MEDIA_ROOT, self.filename))
        elif self.type == 2: # Video
            delfile("%sv/thumb/%s.jpg" % (settings.MEDIA_ROOT, self.filename))
            delfile("%sv/%s" % (settings.MEDIA_ROOT, self.filename))
        elif self.type == 3: # Audio
            delfile("%sa/%s" % (settings.MEDIA_ROOT, self.filename))
        elif self.type == 4: # Flash
            delfile("%sf/thumb/%s.jpg" % (settings.MEDIA_ROOT, self.filename))
            delfile("%sf/%s" % (settings.MEDIA_ROOT, self.filename))
        super(LibraryFile, self).delete()

    def thumbnail_url(self):
        filename = self.filename if self.type == 1 else self.filename + '.jpg'
        if self.type == 1: folder = 'i'
        elif self.type == 2: folder = 'v'
        elif self.type == 3:
            return settings.MEDIA_URL + 'audio.jpg'
        elif self.type == 4: folder = 'f'
        return settings.MEDIA_URL + folder + '/thumb/' + filename

    def thumbnail(self, width=LIBRARYFILE_THUMB_WIDTH):
        extra_class = 'video' if self.type == 2 else ''
        height = width / LIBRARYFILE_THUMB_RATIO
        return u'<div title="%s" class="adexthumb" style="width:%dpx;height:%dpx;"><div class="%s" style="background-image:url(%s);"></div></div>' %\
               ('%s - %s' % (self.type_name(), self.name or self.filename),
                width, height, extra_class, self.thumbnail_url())

    def type_name(self):
        return self.MEDIA_CHOICES[self.type-1][1]

    def content_type(self):
        return mimetypes.guess_type(self.filename)[0]

    def url(self):
        return reverse(self.type_name(), args=[self.pk])
#        if self.type == 1:
#            return reverse('image', args=[self.pk])
#        elif self.type == 2:
#            return reverse('video', args=[self.pk])
#        elif self.type == 3:
#            return reverse('audio', args=[self.pk])
#        elif self.type == 4:
#            return reverse('flash', args=[self.pk])
#        else:
#            return False
    
    thumbnail.short_description = 'Thumbnail'
    thumbnail.allow_tags = True
    def __unicode__(self):
        return "%s [%s]" % (self.name or self.filename, self.type_name())