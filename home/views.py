from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from profiles.views import profile_detail
from tagging.models import TaggedItem
from adex.models import Adex
from adex.views import adex_view
from comments.models import AdexComment
from medialibrary.models import LibraryFile
from medialibrary.tagging_utils import get_tag_counts

def index(request):
    #if request.user.is_authenticated():
        #comment_list = Comment.objects.all().order_by('date')
    if len(request.GET) > 0:
        item_code = request.META.get('QUERY_STRING')
        return adex_view(request, item_code)
    else:
        return render_to_response('home/index.html', {'user':request.user}, context_instance=RequestContext(request))

def browse(request, page):
    #adex_list = Adex.objects.all()
    paginator = Paginator(Adex.objects.all().order_by('-date'), 5)
    try:
        p = paginator.page(page)
    except PageNotAnInteger:
        p = paginator.page(1)
    except EmptyPage:
        p = paginator.page(paginator.num_pages)
    return render_to_response('home/browse.html', {'user':request.user, 'page':p}, context_instance=RequestContext(request))

def tagged(request, tag, page):
    adex = TaggedItem.objects.get_by_model(Adex, tag)
    paginator = Paginator(adex, 5)
    try:
        p = paginator.page(page)
    except PageNotAnInteger:
        p = paginator.page(1)
    except EmptyPage:
        p = paginator.page(paginator.num_pages)
    return render_to_response('home/tagged.html', {'user':request.user, 'page':p}, context_instance=RequestContext(request))

def user_home(request):
    return render_to_response('home/mypage.html', {'user':request.user}, context_instance=RequestContext(request))

def profile(request, username):
    user = get_object_or_404(User, username=username)
    adexs = Adex.objects.filter(user=user).order_by('-date')[:4]
    comments = AdexComment.objects.filter(user=user, is_anonymous=False).order_by('-submit_date')[:2]
    media = LibraryFile.objects.filter(user=user).order_by('-date')[:6]
#    if media.count() >= 6:
#        media = media[:6]
    return profile_detail(request, username, extra_context={'adexs':adexs, 'comments':comments, 'media':media})

def image_page(request, file_id):
    image = get_object_or_404(LibraryFile.objects, pk=file_id, type=1)
    tags = get_tag_counts(image)
    return render_to_response('home/media_pages/image.html', {'image':image, 'tags':tags}, RequestContext(request))

def video_page(request, file_id):
    video = get_object_or_404(LibraryFile.objects, pk=file_id, type=2)
    w = 670 if video.width > 670 else video.width
    h = int(w / (video.width / video.height))
    return render_to_response('home/media_pages/video.html', {'video':video, 'video_width':w, 'video_height':h}, RequestContext(request))

def audio_page(request, file_id):
    audio = get_object_or_404(LibraryFile.objects, pk=file_id, type=3)
    return render_to_response('home/media_pages/audio.html', {'audio':audio}, RequestContext(request))

def flash_page(request, file_id):
    flash = get_object_or_404(LibraryFile.objects, pk=file_id, type=4)
    return render_to_response('home/media_pages/flash.html', {'flash':flash}, RequestContext(request))

def album_page(request, file_id):
    album = get_object_or_404(LibraryFile.objects, pk=file_id, type=5)
    return render_to_response('home/media_pages/album.html', {'album':album}, RequestContext(request))

def rss(request):
    items = Adex.objects.all().order_by('-date')[:20]
    return render_to_response('home/rss.xml', {'items':items}, mimetype="application/xhtml+xml")