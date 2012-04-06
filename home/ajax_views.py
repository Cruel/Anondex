import random
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.db.models.aggregates import Count
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template.context import RequestContext
from django.utils import simplejson as json
from django.views.decorators.csrf import csrf_exempt
from tagging.models import Tag
from tagging.utils import calculate_cloud
from adex.models import Adex
from adextagging.models import MyTag
from comments.models import AdexComment
from comments.templatetags.adexcomments import get_thumb_rating
from medialibrary.models import LibraryFile
import tagging

@csrf_exempt
def filelist(request):
    media = request.session.get('uploaded_media') or []
    action = request.GET.get('action')
    media_list, image_list, video_list, audio_list, flash_list, remove_list = ([] for i in range(6))
    if action == 'add':
        media.append(request.GET.get('id'))
    if len(media) > 0:
        if action == 'remove':
            media.remove(request.GET.get('id'))
        for media_id in media:
            try:
                file = LibraryFile.objects.get(pk=media_id)
                media_list.append(file)
                if file.type == 1: image_list.append(file)
                elif file.type == 2: video_list.append(file)
                elif file.type == 3: audio_list.append(file)
                elif file.type == 4: flash_list.append(file)
            except LibraryFile.DoesNotExist:
                remove_list.append(media_id)
        for media_id in remove_list:
            media.remove(media_id)
    request.session['uploaded_media'] = media
    return render_to_response('home/filelist.html',
            {'media_list':media_list, 'files_list':[image_list, video_list, audio_list, flash_list]},
                    context_instance=RequestContext(request))

def taglist(request):
    media = request.session.get('uploaded_media') or []
    available_tags = Tag.objects.all().order_by('name').values_list('name', flat=True)
    assigned_tags = []
    if 'create' in request.META.get('QUERY_STRING'):
        assigned_tags = MyTag.objects.get_tags_from_media(media)
    return HttpResponse(json.dumps({'availableTags':tuple(available_tags),'assignedTags':tuple(assigned_tags)}), mimetype="application/json")

def comment(request, comment_id):
    comment = get_object_or_404(AdexComment.objects, pk = comment_id)
    return render_to_response('comments/comments.html', {'comment_list':[comment],'anchored':False}, RequestContext(request))

def sidebar(request):
    adex_list = Adex.objects.all().order_by('-date')[:2]
    comments = AdexComment.objects.all().order_by('-submit_date')[:3]
    files = LibraryFile.objects.exclude(type=3).exclude(visible=False)
    if files.count() > 6: files = random.sample(files, 6)
    tagcloud = MyTag.objects.annotate(count=Count('id')).filter(items__isnull=False, count__gt=0).order_by('name')
    tagcloud = calculate_cloud(tagcloud, steps=4, distribution=tagging.utils.LOGARITHMIC)
    return render_to_response('home/sidebar.html', {'adex_list':adex_list, 'comment_list':comments, 'rand_files':files, 'tagcloud':tagcloud},
                    context_instance=RequestContext(request))

def rate(request):
    from djangoratings.views import AddRatingView

    if request.POST:
        content_type = ContentType.objects.get(model=request.POST.get('model'))
        response = AddRatingView()(request,
            content_type_id = content_type.id,
            object_id = request.POST.get('id'),
            field_name = 'rating',
            score = request.POST.get('score')
        )
        if response.status_code == 200:
            if response.content == 'Vote recorded.':
    #            request.user.add_xp(settings.XP_BONUSES['submit-rating'])
                print "mmk"
            comment = AdexComment.objects.get(id = request.POST.get('id'))
            return HttpResponse(json.dumps({'success':True, 'value':response.content, 'rating':get_thumb_rating(comment.rating)}))
        return HttpResponse(json.dumps({'success':False, 'value':response.content}))
    else:
        return redirect('/')

def encode_progress(request):
    ip = request.META['REMOTE_ADDR']
    framestring = cache.get('%s_frame'%ip)
    cache.set('%s_frame'%ip, None)
    cache.delete('%s_frame'%ip)
    return HttpResponse(json.dumps({'percent':cache.get('%s_encode'%ip), 'frame':framestring}), mimetype="application/json")