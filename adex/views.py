import random
import string
import urllib2
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template.context import RequestContext
from django.utils import simplejson as json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import condition
from tagging.models import Tag, TaggedItem
import time
from adex.create import processCreateVars, genData, genItemCode
from adex.models import Adex
from home.ajax_views import addlibfile
from medialibrary.models import LibraryFile
from medialibrary.utils import genVideoThumb, webthumb
import settings

def adex_view(request, item_code):
    adex = get_object_or_404(Adex, item_code=item_code)
    ctype = ContentType.objects.get(model="adex")
    tags = Tag.objects.raw('''SELECT t.id, t.name, COUNT(*) as count
          FROM tagging_tag AS t
                  INNER JOIN tagging_taggeditem AS tt ON t.id = tt.tag_id
                  INNER JOIN `adex_adex` ON tt.object_id = `adex_adex`.`id`
          WHERE t.id IN (

            SELECT t.id FROM tagging_tag AS t
        INNER JOIN tagging_taggeditem AS tt ON t.id = tt.tag_id
          WHERE tt.content_type_id = %d AND tt.object_id = %d

                  )
          GROUP BY t.id
          ORDER BY count DESC''' % (ctype.id, adex.id))
    return adex_render(request, adex, tags)


def adex_render(request, adex, tags, media=None):
    if adex.pk: media = adex.media.all()
    related = TaggedItem.objects.get_related(adex, Adex, num=10)
    adex_data = json.loads(adex.data)

    return render_to_response(adex.template(), {'user':request.user, 'adex':adex, 'media_list':media, 'adex_data':adex_data, 'tags':tags, 'related':related},
                                  context_instance=RequestContext(request))

def tagged(request, tag):
    pass

def filelist(request):
    #if request.user.is_authenticated():
        #comment_list = Comment.objects.all().order_by('date')
    items = ''
    return render_to_response('home/index.html', {'user':request.user, 'items':items}, context_instance=RequestContext(request))


@csrf_exempt
def preview(request):
    if request.POST:
        # (re)Verify input
        v = request.POST.copy()
        errors = processCreateVars(v)
        data, media_list = genData(v)
        if not errors:
            user = request.user if request.user.is_authenticated() else None
            adex = Adex(
                user        = user,
                ip          = request.META['REMOTE_ADDR'],
                domain      = v.get('domain'),
                title       = v.get('title'),
                description = v.get('description'),
                type        = v.get('type'),
                tags        = v.get('tags'),
                data        = data,
            )
            media = list()
            tags = list()
            for i in v.get('tags').split(','):
                tags.append(Tag(name=i))
            if len(media_list) > 0:
                for media_id in media_list:
                    media.append(LibraryFile.objects.get(pk=media_id))
            return adex_render(request, adex, tags, media)
        else:
            return HttpResponse('<div><ul><li>'+'</li><li>'.join(errors)+'</li></ul></div>')
    else:
        return redirect('/')


def create_adex(request):
    if request.POST:
        # (re)Verify input
        v = request.POST.copy()
        errors = processCreateVars(v)
        data, media_list = genData(v)
        if not errors:
            user = request.user if request.user.is_authenticated() else None
            adex = Adex.objects.create(
                user        = user,
                ip          = request.META['REMOTE_ADDR'],
                item_code   = genItemCode(),
                domain      = v.get('domain'),
                title       = v.get('title'),
                description = v.get('description'),
                type        = v.get('type'),
                tags        = v.get('tags'),
                data        = data,
            )
            if len(media_list) > 0:
                for media_id in media_list:
                    adex.media.add(LibraryFile.objects.get(pk=media_id))
            if adex.type == 3:
                webthumb(v['url'], settings.MEDIA_ROOT+'webthumb/%d.jpg'%adex.pk)

            try:
                del request.session['uploaded_media']
            except KeyError: pass

            return HttpResponse(json.dumps({'success':True, 'value':'http://anondex.com/?'+adex.item_code}))
        else:
            return HttpResponse(json.dumps({'success':False, 'error':'<div><ul><li>'+'</li><li>'.join(errors)+'</li></ul></div>'}))
    else:
        return redirect('/')


def upload_file(request):
    # TODO: Limit user uploads to avoid upload bombing
    if request.method == 'POST':
        try:
            user = request.user if request.user.is_authenticated() else None
            file = LibraryFile(user=user, ip=request.META['REMOTE_ADDR'])
            file.save_file(request.FILES['file'])
            return addlibfile(request, file.id)
        except Exception, e:
            return HttpResponse(json.dumps({'success':False, 'error':e.message}))
    return HttpResponse(json.dumps({'success':False, 'error':'Error uploading file.'}))





def test_video(request):
    if genVideoThumb('/home/thomas/PycharmProjects/anondex/media/v/test.webm','/home/thomas/PycharmProjects/anondex/media/v/test.jpg'):
        return HttpResponse('Success')
    else:
        return HttpResponse('Failure')

import urlparse
@condition(etag_func=None)
def steam(request):
    #return render_to_response('adex/base.html', {'user':request.user}, context_instance=RequestContext(request))
    data = urllib2.urlopen('http://youtube.com/get_video_info?video_id=tc0Wtm180G4').read()
    v = urlparse.parse_qs(data)
    fmts = v['url_encoded_fmt_stream_map'][0].split(',')
    #l = urlparse.parse_qs(v['url_encoded_fmt_stream_map'][0])
    #fmt_list = urlparse.parse_qs(urllib2.unquote(l[0]))
    fmt_list = urlparse.parse_qs(fmts[0])
    return HttpResponse(fmt_list['url'], mimetype="text/html")
    #return HttpResponse( streamer(), mimetype='text/html')

def streamer():
    yield "<html><body>\n"
    for x in range(1,11):
        yield "<div>%s</div>\n" % x
        yield " " * 1024  # Encourage browser to render incrementally
        time.sleep(1)
    yield "</body></html>\n"