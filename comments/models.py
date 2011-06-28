from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class UserProfile(models.Model):
    url = models.URLField()
    home_address = models.TextField()
    phone_numer = models.IntegerField()
    user = models.ForeignKey(User, unique=True)

class User(models.Model):
    ip = models.CharField(unique=True, max_length=45)
    #ip = models.GenericIPAddressField()
    country = models.CharField(max_length=96, blank=True)
    countrycode = models.CharField(max_length=48, blank=True)
    city = models.CharField(max_length=192, blank=True)
    region = models.CharField(max_length=48, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    agent = models.TextField(blank=True)
    def __unicode__(self):
        return self.ip

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

class Comment(models.Model):
    item_id = models.IntegerField()
    name = models.CharField(max_length=75)
    hash = models.CharField(max_length=24, null=True, blank=True)
    comment = models.TextField()
    image = models.ForeignKey(Image, null=True)
    image_status = models.IntegerField(null=True, blank=True)
    date = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(User)
    is_mod = models.BooleanField()
    in_image = models.IntegerField()
    rating = models.IntegerField()
    def __unicode__(self):
        return self.comment

#class Poll(models.Model):
#    question = models.CharField(max_length=200)
#    pub_date = models.DateTimeField('date published')
#    def was_published_today(self):
#        return self.pub_date.date() == datetime.date.today()
#    was_published_today.short_description = 'Published today?'
#    def __unicode__(self):
#        return self.question
#
#class Choice(models.Model):
#    poll = models.ForeignKey(Poll)
#    choice = models.CharField(max_length=200)
#    votes = models.IntegerField()
#    def __unicode__(self):
#        return self.choice
