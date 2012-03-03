from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from medialibrary.models import LibraryFile

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