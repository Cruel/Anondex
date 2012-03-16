from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from medialibrary.models import LibraryFile
from django.utils import simplejson as json

def flashview(request):
    url = request.META.get('QUERY_STRING')
    return render_to_response('medialibrary/flashview.html', {'flashurl':url}, RequestContext(request))

def index(request):
    #if request.user.is_authenticated():
        #comment_list = Comment.objects.all().order_by('date')
    items = ''
    return render_to_response('home/index.html', {'user':request.user, 'items':items}, context_instance=RequestContext(request))

#@login_required
def attach(request):
    files = LibraryFile.objects.all().order_by('date')
    return render_to_response('medialibrary/attach.html', {'user':request.user, 'files':files}, context_instance=RequestContext(request))

def upload_file(request):
    # TODO: Limit user uploads to avoid upload bombing
    if request.method == 'POST':
        try:
            user = None
            if request.POST.get('user')=='name' and request.user.is_authenticated():
                user = request.user
            file = LibraryFile(user=user, ip=request.META['REMOTE_ADDR'], tags=request.POST.get('tags'))
            file.save_file(request.FILES['file'])
            return HttpResponse(json.dumps({
                'success'   :True,
                'id'        :file.id,
                'url'       :'http://anondex.com'+file.url(),
                'thumb'     :file.thumbnail(),
            }))
        except Exception, e:
            return HttpResponse(json.dumps({'success':False, 'error':e.message}))
    return HttpResponse(json.dumps({'success':False, 'error':'Error uploading file.'}))