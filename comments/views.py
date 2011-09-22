from django.contrib.auth.decorators import login_required
from django.core.files.move import file_move_safe
from django.shortcuts import get_object_or_404, render_to_response, get_list_or_404, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import RequestContext
from adex.models import Adex
from comments.models import AdexComment
from django.core.cache import cache
from django.utils import simplejson
from medialibrary.models import LibraryFile
import settings

def index(request):
    if request.user.is_authenticated():
        comment_list = AdexComment.objects.all().order_by('date')
        return render_to_response('comments/index.html', {'comment_list':comment_list, 'user':request.user})
    else:
        return HttpResponse('<p><a href="/accounts/login">Sign in with OpenID</a></p><p><a href="/private">This requires authentication</a></p>')

def detail(request, item_id):
    adex = get_object_or_404(Adex, pk=item_id)
    #comments = get_list_or_404(AdexComment.objects.select_related().order_by('date'), item_id=comment_id, in_image=0)
    return render_to_response('comments/adex.html', {'item':adex}, context_instance=RequestContext(request))

def test(request):
    c = get_list_or_404(AdexComment.objects.select_related().order_by('date'), item_id=comment_id, in_image=0)
    return render_to_response('comments/detail.html', {'comments':c},
                               context_instance=RequestContext(request))

def image_page(request, image_id):
    image = get_object_or_404(LibraryFile.objects, pk = image_id)
#    c = Comment.objects.order_by('date').filter()
    return render_to_response('comments/image.html', {'image':image},
                               context_instance=RequestContext(request))

@login_required
def require_authentication(request):
    return HttpResponse('This page requires authentication')

def upload_image(request):
    if request.method == 'POST':
        try:
            file = LibraryFile(user=request.user, ip=request.META['REMOTE_ADDR'])
            file.save_file(request.FILES['imagefile'])
            return HttpResponse(simplejson.dumps({'success':True, 'value':file.id}))
        except Exception, e:
            return HttpResponse(simplejson.dumps({'success':False, 'error':e.message}))
    else:
        redirect('/')