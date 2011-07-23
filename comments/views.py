from django.contrib.auth.decorators import login_required
from django.core.files.move import file_move_safe
from django.shortcuts import get_object_or_404, render_to_response, get_list_or_404
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import RequestContext
from comments.models import User, Image, Comment
from django.core.cache import cache
from django.utils import simplejson
from PIL import Image as pil
from comments.utils import md5_file
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
    image = get_object_or_404(Image.objects, pk = image_id)
#    c = Comment.objects.order_by('date').filter()
    return render_to_response('comments/image.html', {'image':image},
                               context_instance=RequestContext(request))

@login_required
def require_authentication(request):
    return HttpResponse('This page requires authentication')

def upload_image(request):
    if request.method == 'POST':
        EXTENSION_CHOICES = {
            'image/jpeg':   1,
            'image/png':    2,
            'image/gif':    3,
        }
        f = request.FILES['imagefile']
        if f.content_type in EXTENSION_CHOICES:
            ext = EXTENSION_CHOICES[f.content_type]
            path = settings.MEDIA_ROOT + 'tmp/' + f.name
            destination = open(path, 'wb+')
            print "Opened %s for writing as %s..." % (path, f.content_type)
            for chunk in f.chunks():
                destination.write(chunk)
            destination.close()

            im = pil.open(path)
            (width, height) = im.size
            md5 = md5_file(path)

            # If image md5 doesn't already exist, make the image
            try:
                image = Image.objects.get(md5=md5)
            except Image.DoesNotExist:
                image = Image(width=width, height=width, md5=md5, name=f.name)
                image.save()
                im.thumbnail((100,100), pil.ANTIALIAS)
                image.name = "adex%s_%s" % (image.id, f.name)
                im.save(settings.MEDIA_ROOT + "i/thumb/%s" % image.name)
                file_move_safe(path,settings.MEDIA_ROOT + "i/%s" % image.name)
                image.save()
            print image.id
            return HttpResponse(simplejson.dumps({'success':True, 'value':image.id}))
        return HttpResponse(simplejson.dumps({'success':False, 'error':'Not a valid image.'}))
    return HttpResponse(simplejson.dumps({'success':False, 'error':'Error uploading file.'}))

def get_upload_progress(request):
    """
    Return JSON object with information about the progress of an upload.
    """
    progress_id = request.GET['x-id']
    if progress_id:
        cache_key = "%s_%s" % (request.META['REMOTE_ADDR'], progress_id)
        data = cache.get(cache_key)
        print "Returning progress data: %s" % data
        return HttpResponse(simplejson.dumps(data))
    else:
        return HttpResponseBadRequest('Server Error: You must provide X-Progress-ID header or query param.')