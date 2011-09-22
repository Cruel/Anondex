from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from adex.models import Adex
from adex.views import adex_view

def index(request):
    #if request.user.is_authenticated():
        #comment_list = Comment.objects.all().order_by('date')
    if len(request.GET) > 0:
        item_code = list(request.GET.viewkeys())[0]
        return adex_view(request, item_code)
    else:
        return render_to_response('home/index.html', {'user':request.user}, context_instance=RequestContext(request))

def browse(request, page):
    #adex_list = Adex.objects.all()
    paginator = Paginator(Adex.objects.all(), 5)
    try:
        p = paginator.page(page)
    except PageNotAnInteger:
        p = paginator.page(1)
    except EmptyPage:
        p = paginator.page(paginator.num_pages)
    return render_to_response('home/browse.html', {'user':request.user, 'page':p}, context_instance=RequestContext(request))

def user_home(request):
    return render_to_response('home/mypage.html', {'user':request.user}, context_instance=RequestContext(request))