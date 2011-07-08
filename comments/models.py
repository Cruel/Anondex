from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.contrib.comments.models import Comment
from django.contrib.comments.views import comments
from django.contrib.comments.signals import comment_will_be_posted
from django.dispatch.dispatcher import receiver


class Image(models.Model):
    width = models.IntegerField()
    height = models.IntegerField()
    ext = models.TextField(blank=True)
    md5 = models.TextField(blank=True)
    rating = models.FloatField(default=0.0)
    rating_total = models.IntegerField(default=0)
    vote_count = models.IntegerField(default=0)
    image = models.ImageField(upload_to='p', height_field='height', width_field='width')
    def save(self):
        # TODO: make thumbnail here?
        self.md5 = "test"
        super(Image, self).save()
        pass
    def __unicode__(self):
        return self.md5+'.'+self.ext

class AdexComment(Comment):
    title = models.CharField(max_length=300)
    image = models.ForeignKey(Image, null=True)

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

@receiver(comment_will_be_posted, sender=AdexComment)
def my_callback(sender, comment, request, **kwargs):
    print "my_callback"
    #comment.comment = "LOCHANGED2"