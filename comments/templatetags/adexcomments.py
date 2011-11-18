from __future__ import division
from django import template
from comments.models import AdexComment
from comments.utils import get_fancy_time, GetInHMS
import postmarkup
register = template.Library()

@register.filter
def timeago(value):
    return get_fancy_time(value)

@register.filter
def bbcode(value):
    return adex_bbcode(value)

@register.filter
def get_thumb_rating(ratingmanager):
    if ratingmanager.votes == 0: return 0
    percent_upvote = (ratingmanager.score - ratingmanager.votes) / ratingmanager.votes
    upvotes = (percent_upvote) * ratingmanager.votes
    downvotes = ratingmanager.votes - upvotes
    return int(upvotes - downvotes)

class CommentTag(postmarkup.ImgTag):
    def render_open(self, parser, node_index, **kwargs):
        c = self.get_contents(parser)
        self.skip_contents(parser)
        try:
            comment = AdexComment.objects.get(pk = c)
            url = comment.content_object.url()
        except AdexComment.DoesNotExist:
            #TODO: remove [c] tags in db comment so this is never called again
            return '@%s' % c
        return u'<a class="reply no-ajaxy" onclick="return hltag(\'%(id)s\');" rel="#%(id)s" href="%(url)s#%(id)s">@%(id)s</a>' % \
               {'id':c, 'url':url}

class VideoTag(postmarkup.ImgTag):
    def render_open(self, parser, node_index, **kwargs):
        video_time = self.get_contents(parser)
        self.skip_contents(parser)
        return u'<a href="javascript:vidseek(%s);">%s</a>' % (video_time, GetInHMS(video_time))

adex_bbcode = postmarkup.create()
adex_bbcode.add_tag(CommentTag, u"c")
adex_bbcode.add_tag(VideoTag, u"v")