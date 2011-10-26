import urllib2
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template.context import RequestContext
from django.utils import simplejson as json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import condition
from tagging.models import Tag, TaggedItem
import time
from adex.models import Adex
from medialibrary.models import LibraryFile
from medialibrary.utils import genVideoThumb
import settings

def adex_view(request, item_code):
    adex = get_object_or_404(Adex, item_code=item_code)

    tags = Tag.objects.raw('''SELECT t.id, t.name, COUNT(*) as count
          FROM tagging_tag AS t
                  INNER JOIN tagging_taggeditem AS tt ON t.id = tt.tag_id
                  INNER JOIN `adex_adex` ON tt.object_id = `adex_adex`.`id`
          WHERE t.id IN (

            SELECT t.id FROM tagging_tag AS t
        INNER JOIN tagging_taggeditem AS tt ON t.id = tt.tag_id
          WHERE tt.content_type_id = 20 AND tt.object_id = %d

                  )
          GROUP BY t.id
          ORDER BY count DESC''' % adex.id)
    return adex_render(request, adex, tags)


def adex_render(request, adex, tags, media=None):
    if not media: media = adex.media.all()
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
            adex = Adex(
                user        = request.user,
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
                tags.append(Tag.objects.get(name=i))
            if len(media_list) > 0:
                for media_id in media_list:
                    media.append(LibraryFile.objects.get(pk=media_id))
            return adex_render(request, adex, tags, media)
        else:
            return HttpResponse('<div><ul><li>'+'</li><li>'.join(errors)+'</li></ul></div>')
    else:
        return redirect('/')

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

def processCreateVars(vars):
    errors = list()
    for i in vars.keys():
        if vars[i] == 'undefined': vars[i] = ''
    if not vars.get('title'): errors.append('"Title" must be defined.')
    if not vars.get('description'): errors.append('"Description" must be defined.')
    if not vars.get('tags'): errors.append('You must supply some tags.')
    if not vars.get('type'): errors.append('You must select a template.')
    if not vars.get('name'):
        pass # check name availability
    if vars.get('type') == '0':
        if not vars.get('imgtemplate'): errors.append('You must select an image template layout.')
        if not vars.get('imageselect'): errors.append('You must upload an image.')
    elif vars.get('type') == '1':
        if not vars.get('videoselect'): errors.append('You must upload an image.')
    elif vars.get('type') == '2':
        if not vars.get('url'): errors.append('You must define a URL.')
    elif vars.get('type') == '3':
        if not vars.get('htmlselect') and not vars.get('html'):
            errors.append('You must upload an HTML file, or input custom HTML.')
    elif vars.get('type') == '4':
        if not vars.get('flashselect'): errors.append('You must upload a flash (.swf) file.')
    if vars.get('preview') == '0' and not vars.get('recaptcha_response_field'):
        errors.append('Captcha must be completed.')
    # TODO: More checks... for valid files, valid url, etc... ?
    return errors if len(errors) > 0 else False


def genItemCode():
    return '5oS'


# {"image":{"style":"stretch","proportional":true},"audio":null}
def genData(vars):
    #ret = {"image":{"style":"stretch","proportional":True},"audio":None}
    if vars['type'] == '0':
        ret = {"image":{},"audio":{}}
        ret['image']['id'] = int(vars['imageselect'])
        media = [ret['image']['id']]
        if vars.get('audioselect'):
            ret['audio']['id'] = int(vars['audioselect'])
            media.append(ret['audio']['id'])
        if vars['imgtemplate'] == '1': ret['image']['style'] = 'center'
        elif vars['imgtemplate'] == '2': ret['image']['style'] = 'tile'
        elif vars['imgtemplate'] == '3': ret['image']['style'] = 'stretch'
        ret['image']['proportional'] = vars['proportional'] == 'yes'
    elif vars['type'] == '1':
        ret = {'video':{'id':int(vars['videoselect'])}}
        media = [ret['video']['id']]
    else:
        ret = {}
        media = []
    return json.dumps(ret), media



@csrf_exempt
def create_adex(request):
    if request.POST:
        # (re)Verify input
        v = request.POST.copy()
        errors = processCreateVars(v)
        data, media_list = genData(v)
        if not errors:
            adex = Adex.objects.create(
                user        = request.user,
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

#            if media_list and len(media_list) > 0:
#                for media_id in media_list:
#                    if adex.type == '0':
#                        if (media_id == v.get('imageselect')) or (media_id == v.get('audioselect')):
#                            adex.media.add(LibraryFile.objects.get(pk=media_id))
            try:
                del request.session['uploaded_media']
            except KeyError: pass

            return HttpResponse('Success!')
        else:
            return HttpResponse('<div><ul><li>'+'</li><li>'.join(errors)+'</li></ul></div>')
    else:
        return redirect('/')


def upload_file(request):
    # TODO: Limit user uploads to avoid upload bombing
    if request.method == 'POST':
        try:
            file = LibraryFile(user=request.user, ip=request.META['REMOTE_ADDR'])
            file.save_file(request.FILES['file'])
            media = request.session.get('uploaded_media') or []
            media.append(unicode(file.id))
            request.session['uploaded_media'] = media
            return HttpResponse(json.dumps({'success':True, 'value':file.id}))
        except Exception, e:
            return HttpResponse(json.dumps({'success':False, 'error':e.message}))
    return HttpResponse(json.dumps({'success':False, 'error':'Error uploading file.'}))

def test_video(request):
    if genVideoThumb('/home/thomas/PycharmProjects/anondex/media/v/test.webm','/home/thomas/PycharmProjects/anondex/media/v/test.jpg'):
        return HttpResponse('Success')
    else:
        return HttpResponse('Failure')