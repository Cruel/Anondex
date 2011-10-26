from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt
from tagging.models import Tag
from adex.models import Adex
from comments.models import AdexComment
from medialibrary.models import LibraryFile

@csrf_exempt
def filelist(request):
    media = request.session.get('uploaded_media')
    media_list, image_list, video_list, audio_list, flash_list, remove_list = ([] for i in range(6))
    if media and len(media) > 0:
        if request.GET.get('d'):
            media.remove(request.GET.get('d'))
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
    tags = Tag.objects.all().order_by('name').values_list('name', flat=True)
    return HttpResponse(simplejson.dumps({'availableTags':tuple(tags),'assignedTags':()}))

def sidebar(request):
    adex_list = Adex.objects.all().order_by('-date')[:1]
    comments = AdexComment.objects.all().order_by('-submit_date')[:4]
    files = LibraryFile.objects.all().order_by('-date')[:4]
    return render_to_response('home/sidebar.html', {'adex_list':adex_list, 'comment_list':comments, 'rand_files':files},
                    context_instance=RequestContext(request))