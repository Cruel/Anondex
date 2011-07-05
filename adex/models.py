from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

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
    item_code = models.CharField(max_length=12)
    domain = models.CharField(max_length=90, null=True, blank=True)
    title = models.CharField(max_length=90)
    description = models.TextField()
    date = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(User)
    rating = models.FloatField(default=0.0)
    rating_total = models.IntegerField(default=0)
    vote_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    content_rating = models.PositiveSmallIntegerField(choices=CONTENT_RATING, default=0)
    status = models.PositiveSmallIntegerField(choices=STATUS, default=0)
    type = models.PositiveSmallIntegerField(choices=CONTENT_TYPE)
    data = models.TextField()
    def __unicode__(self):
        return self.title


class AdexTempInfo(models.Model):
    adex = models.ForeignKey(Adex)
    expiration = models.IntegerField()
    dead = models.IntegerField()
    redeemval = models.IntegerField()
    def __unicode__(self):
        return self.adex.title