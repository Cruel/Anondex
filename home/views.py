from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext

def index(request):
    if request.user.is_authenticated():
        #comment_list = Comment.objects.all().order_by('date')
        return render_to_response('home/index.html', {'user':request.user}, context_instance=RequestContext(request))
    else:
        return HttpResponse('<p><a href="/socialauth/login">Sign in with OpenID</a></p><p><a href="/private">This requires authentication</a></p>')