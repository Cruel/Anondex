from django.contrib.auth.decorators import login_required
from django.core.files.move import file_move_safe
from django.shortcuts import get_object_or_404, render_to_response, get_list_or_404
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import RequestContext
from comments.models import User, Comment
from django.core.cache import cache
from django.utils import simplejson
from PIL import Image as pil
from comments.utils import md5_file
from medialibrary.models import LibraryFile
from medialibrary.utils import ProcessLibraryImage
import settings

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
        EXTENSION_CHOICES = ( 'image/jpeg', 'image/png', 'image/gif',)
        f = request.FILES['imagefile']
        if f.content_type in EXTENSION_CHOICES:
            path = settings.MEDIA_ROOT + 'tmp/' + f.name
            destination = open(path, 'wb+')
            print "Opened %s for writing as %s..." % (path, f.content_type)
            for chunk in f.chunks():
                destination.write(chunk)
            destination.close()
            imageid = ProcessLibraryImage(path)

            return HttpResponse(simplejson.dumps({'success':True, 'value':imageid}))
        return HttpResponse(simplejson.dumps({'success':False, 'error':'Not a valid image.'}))
    return HttpResponse(simplejson.dumps({'success':False, 'error':'Error uploading file.'}))