# Anondex Reporting APP is a modified version of 'django-flag'. My thanks to any devs of that project.

from datetime import datetime

from django.db import models

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from django.contrib.auth.models import User, AnonymousUser


STATUS = (
    ('1', 'flagged'),
    ('2', 'flag rejected by moderator'),
    ('3', 'creator notified'),
    ('4', 'content removed by creator'),
    ('5', 'content removed by moderator'),
)

# Can change order, but not numbers
REPORT_TYPE = (
    ('1', 'Spam'),
    ('2', 'Porn'),
    ('3', 'Advertising'),
    ('4', 'Copyrighted'),
    ('5', 'Illegal'),
    ('0', 'Other'), # Other must be 0
)

class FlaggedContent(models.Model):
    
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    
    creator = models.ForeignKey(User, null=True, related_name="flagged_content") # user who created flagged content -- this is kept in model so it outlives content
    status = models.CharField(max_length=1, choices=STATUS, default='1')    
    moderator = models.ForeignKey(User, null=True, related_name="moderated_content") # moderator responsible for last status change


class FlagInstance(models.Model):
    
    flagged_content = models.ForeignKey(FlaggedContent)
    user = models.ForeignKey(User, null=True) # user flagging the content
    ip = models.IPAddressField()
    when_added = models.DateTimeField(default=datetime.now)
    when_recalled = models.DateTimeField(null=True) # if recalled at all
    type  = models.PositiveSmallIntegerField(choices=REPORT_TYPE, default=0)
    comment = models.TextField(null=True) # comment by the flagger

    class Meta:
        unique_together = (("flagged_content", "ip"),)


def add_flag(flagger, content_type, object_id, content_creator, comment, report_type, ip):
    
    # check if it's already been flagged
    try:
        flagged_content = FlaggedContent.objects.get(content_type=content_type, object_id=object_id)
    except FlaggedContent.DoesNotExist:
        flagged_content = FlaggedContent(content_type=content_type, object_id=object_id, creator=content_creator)
        flagged_content.save()

    if isinstance(flagger, AnonymousUser):
        flagger = None

    try:
        flag_instance = FlagInstance.objects.get(flagged_content=flagged_content, ip=ip)
        flag_instance.comment = comment
        flag_instance.type = report_type
    except FlagInstance.DoesNotExist:
        flag_instance = FlagInstance(flagged_content=flagged_content, user=flagger, comment=comment, ip=ip, type=report_type)
    flag_instance.save()
    
    return flag_instance
