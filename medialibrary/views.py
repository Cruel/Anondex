from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext

def index(request):
    #if request.user.is_authenticated():
        #comment_list = Comment.objects.all().order_by('date')
    items = ''
    return render_to_response('home/index.html', {'user':request.user, 'items':items}, context_instance=RequestContext(request))