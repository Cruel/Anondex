from django import template
from comments.utils import get_fancy_time, GetInHMS
import postmarkup
register = template.Library()

@register.filter
def timeago(value):
    return get_fancy_time(value)

@register.filter
def bbcode(value):
    return adex_bbcode(value)

class CommentTag(postmarkup.ImgTag):
#    def __init__(self, name,  **kwargs):
#        postmarkup.TagBase.__init__(self, name, inline=True, enclosed=True)
    def render_open(self, parser, node_index, **kwargs):
        # TODO: finish this...
        c = self.get_contents(parser)
        self.skip_contents(parser)
        return u'<a class="reply" onclick="return hltag(\'%s\');" rel="#%s" href="#fix_me">@%s</a>' % (c,c,c)

class VideoTag(postmarkup.ImgTag):
    def render_open(self, parser, node_index, **kwargs):
        video_time = self.get_contents(parser)
        self.skip_contents(parser)
        return u'<a href="javascript:vidseek(%s);">%s</a>' % (video_time, GetInHMS(video_time))

adex_bbcode = postmarkup.create()
adex_bbcode.add_tag(CommentTag, u"c")
adex_bbcode.add_tag(VideoTag, u"v")