from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render_to_response, get_list_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from comments.models import User, Image, Comment

def index(request):
    if request.user.is_authenticated():
        comment_list = Comment.objects.all().order_by('date')
        return render_to_response('comments/index.html', {'comment_list':comment_list, 'user':request.user})
    else:
        return HttpResponse('<p><a href="/accounts/login">Sign in with OpenID</a></p><p><a href="/private">This requires authentication</a></p>')

def detail(request, comment_id):
    c = get_list_or_404(Comment.objects.select_related().order_by('date'), item_id=comment_id, in_image=0)
    return render_to_response('comments/detail.html', {'comments':c},
                               context_instance=RequestContext(request))

def test(request):
    c = get_list_or_404(Comment.objects.select_related().order_by('date'), item_id=comment_id, in_image=0)
    return render_to_response('comments/detail.html', {'comments':c},
                               context_instance=RequestContext(request))

@login_required
def require_authentication(request):
    return HttpResponse('This page requires authentication')