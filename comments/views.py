from django.shortcuts import get_object_or_404, render_to_response, get_list_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from comments.models import User, Image, Comment

def index(request):
    comment_list = Comment.objects.all().order_by('date')
    return render_to_response('comments/index.html', {'comment_list': comment_list})

def detail(request, comment_id):
    c = get_list_or_404(Comment.objects.select_related().order_by('date'), item_id=comment_id, in_image=0)
    return render_to_response('comments/detail.html', {'comments':c},
                               context_instance=RequestContext(request))