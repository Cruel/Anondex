from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils import simplejson
from adex.models import Adex
import settings

def filelist(request):
    #if request.user.is_authenticated():
        #comment_list = Comment.objects.all().order_by('date')
    items = ''
    return render_to_response('home/index.html', {'user':request.user, 'items':items}, context_instance=RequestContext(request))

def preview(request):
    return render_to_response('adex/base.html', {'user':request.user}, context_instance=RequestContext(request))

def upload_file(request):
    if request.method == 'POST':
        VALID_EXTENSIONS = (
            'image/jpeg','image/png','image/gif',
        )
        f = request.FILES['file']
        if f.content_type in VALID_EXTENSIONS:
            path = settings.MEDIA_ROOT + 'test/' + f.name
            destination = open(path, 'wb+')
            print "Opened %s for writing as %s..." % (path, f.content_type)
            for chunk in f.chunks():
                destination.write(chunk)
            destination.close()

            #adex = Adex(item_code='test', user=request.user)
            #adex.save()

            return HttpResponse(simplejson.dumps({'success':True}))
        return HttpResponse(simplejson.dumps({'success':False, 'error':'Not a valid file content type: '+f.name}))
    return HttpResponse(simplejson.dumps({'success':False, 'error':'Error uploading file.'}))