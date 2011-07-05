from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.contrib.comments.models import Comment

class AdexComment(Comment):
    title = models.CharField(max_length=300)

class Image(models.Model):
    width = models.IntegerField()
    height = models.IntegerField()
    ext = models.TextField()
    md5 = models.TextField()
    rating = models.FloatField()
    rating_total = models.IntegerField()
    vote_count = models.IntegerField()
    test1 = models.ImageField(upload_to='i', height_field='height', width_field='width')
    def __unicode__(self):
        return self.md5+'.'+self.ext

#class Comment(models.Model):
#    item_id = models.IntegerField()
#    name = models.CharField(max_length=75)
#    hash = models.CharField(max_length=24, null=True, blank=True)
#    comment = models.TextField()
#    image = models.ForeignKey(Image, null=True)
#    image_status = models.IntegerField(null=True, blank=True)
#    date = models.DateTimeField(default=datetime.now)
#    user = models.ForeignKey(User)
#    is_mod = models.BooleanField()
#    in_image = models.IntegerField()
#    rating = models.IntegerField()
#    def __unicode__(self):
#        return self.comment