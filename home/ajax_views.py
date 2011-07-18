from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def filelist(request):
    result = '<div style="display:none">'
    result+= '<div id="imagelist"><b>Image File:<font class="required">*</font></b> <select id="imageselect">%s</select></div>' % ''
    result+= '<div id="musiclist"><b>Background Music:</b> <select id="musicselect">%s</select></div>' % ''
    result+= '<div id="videolist"><b>Video File:</b> <select id="videoselect">%s</select></div>' % ''
    result+= '<div id="flashlist"><b>Flash File:</b> <select id="flashselect">%s</select></div>' % ''
    result+= '<div id="htmllist"><b>HTML File:</b> <select id="htmlselect">%s</select></div>' % ''
    result+= '<div id="maxfileval">0</div>'
    result+= '</div>'
    return HttpResponse(result)

def taglist(request):
    return HttpResponse(simplejson.dumps({'availableTags':('test1','test2',), 'assignedTags':()}))