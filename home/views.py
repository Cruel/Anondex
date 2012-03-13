from __future__ import division
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from profiles.views import profile_detail
from tagging.models import TaggedItem, Tag
from adex.models import Adex
from adex.views import adex_view
from adextagging.models import MyTag
from comments.models import AdexComment
from home.query_utils import QuerySetSequence
from medialibrary.models import LibraryFile

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

def tagged(request, tags_string):
    tags = tags_string.split('+')
    page = request.GET.get('page') or 1
    adex = TaggedItem.objects.get_by_model(Adex, tags)
    media = TaggedItem.objects.get_by_model(LibraryFile, tags)
    results = QuerySetSequence(media, adex)
    p = Paginator(results, 100)
    try:
        p_results = p.page(page)
    except PageNotAnInteger:
        p_results = p.page(1)
    except EmptyPage:
        p_results = p.page(paginator_adex.num_pages)
    related_tags = MyTag.objects.get_related(tags)
    c = {
#        'user'          :request.user,
        'page'          :p_results,
        'tags_string'   :tags_string,
        'tags'          :tags,
        'related_tags'  :related_tags,
    }
    return render_to_response('home/tagged.html', c, context_instance=RequestContext(request))

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
    tags = MyTag.objects.get_tag_counts(image)
    return render_to_response('home/media_pages/image.html', {'object':image, 'tags':tags}, RequestContext(request))

def video_page(request, file_id):
    video = get_object_or_404(LibraryFile.objects, pk=file_id, type=2)
    w = 670 if video.width > 670 else video.width
    h = int(w / (video.width / video.height))
    tags = MyTag.objects.get_tag_counts(video)
    return render_to_response('home/media_pages/video.html', {'object':video, 'video_width':w, 'video_height':h, 'tags':tags}, RequestContext(request))

def audio_page(request, file_id):
    audio = get_object_or_404(LibraryFile.objects, pk=file_id, type=3)
    tags = MyTag.objects.get_tag_counts(audio)
    return render_to_response('home/media_pages/audio.html', {'object':audio, 'tags':tags}, RequestContext(request))

def flash_page(request, file_id):
    flash = get_object_or_404(LibraryFile.objects, pk=file_id, type=4)
    tags = MyTag.objects.get_tag_counts(flash)
    return render_to_response('home/media_pages/flash.html', {'object':flash, 'tags':tags}, RequestContext(request))

def album_page(request, file_id):
    album = get_object_or_404(LibraryFile.objects, pk=file_id, type=5)
    tags = MyTag.objects.get_tag_counts(album)
    return render_to_response('home/media_pages/album.html', {'object':album, 'tags':tags}, RequestContext(request))

def rss(request):
    items = Adex.objects.all().order_by('-date')[:20]
    return render_to_response('home/rss.xml', {'items':items}, mimetype="application/xhtml+xml")