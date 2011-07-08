from django.contrib.auth.decorators import login_required
from django.dispatch.dispatcher import receiver
from django.shortcuts import get_object_or_404, render_to_response, get_list_or_404
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from comments.forms import AdexCommentForm, ImageUploadForm
from comments.models import User, Image, Comment
from django.core.cache import cache
from django.utils import simplejson
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

@login_required
def require_authentication(request):
    return HttpResponse('This page requires authentication')

def upload(request):
    id = request.POST['id']
    path = settings.MEDIA_ROOT+'%s' % id
    f = request.FILES['picture']
    destination = open(path, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()

def upload2(request):
    if request.method == 'POST':
        form = AdexCommentForm(request.POST, request.FILES)
        if form.is_valid():
#            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/success/url/')
    else:
        form = AdexCommentForm()
#    return render_to_response('upload.html', {'form': form})

def get_upload_progress(request):
    """
    Return JSON object with information about the progress of an upload.
    """
    progress_id = request.GET['X-Progress-ID']
    if progress_id:
        cache_key = "%s_%s" % (request.META['REMOTE_ADDR'], progress_id)
        data = cache.get(cache_key)
        return HttpResponse(simplejson.dumps(data))
    else:
        return HttpResponseBadRequest('Server Error: You must provide X-Progress-ID header or query param.')

def upload_image(request):
    form = ImageUploadForm(request.POST, request.FILES)
    if request.method == 'POST' and form.is_valid():
        image = form.cleaned_data['image']
        image2 = Image(
            image = image,
        )
        image2.save()
        #print form.cleaned_data['image']
        return HttpResponseRedirect('/')