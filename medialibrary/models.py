from django.db import models
from tagging.fields import TagField
from tagging.utils import parse_tag_input

class LibraryFile(models.Model):
    MEDIA_CHOICES = (
        (1, 'image'),
        (2, 'video'),
        (3, 'audio'),
        (4, 'flash'),
    )
    type = models.PositiveSmallIntegerField(choices=MEDIA_CHOICES, default=0)
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    length = models.IntegerField(null=True, blank=True)
    filesize = models.IntegerField(default=100)
    md5 = models.CharField(max_length=60, unique=True)
    name = models.CharField(max_length=60)
    filename = models.CharField(max_length=60)
    tags = TagField()
    def get_tag_list(self):
        return parse_tag_input(self.tags)
    def save(self):
        super(LibraryFile, self).save()
    def delete(self):
        # Remove file if it is not used by any other Adex
        super(LibraryFile, self).delete()
    def __unicode__(self):
        return self.name or self.filename