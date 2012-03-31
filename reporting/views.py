from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404, render_to_response
from django.template.context import RequestContext

from reporting.models import add_flag, REPORT_TYPE

#@login_required
def flag(request, content_type, object_id, creator_field):
    if request.POST:
        report_type = request.POST.get("type")
        comment = request.POST.get("comment")
        next = request.POST.get("next")
        ip = request.META['REMOTE_ADDR']

        content_type = get_object_or_404(ContentType, id = int(content_type))
        object_id = int(object_id)

        content_object = content_type.get_object_for_this_type(id=object_id)

        if creator_field and hasattr(content_object, creator_field):
            creator = getattr(content_object, creator_field)
        else:
            creator = None

        if report_type == '0' and not comment:
            return render_to_response('reporting/form.html', {'message':"You didn't give a reason in your report. Are you stupid?", 'button':'Yes'}, RequestContext(request))

        try:
            add_flag(request.user, content_type, object_id, creator, comment, report_type, ip)
            #request.user.message_set.create(message="You have added a flag. A moderator will review your submission shortly.")
        except Exception, e:
            return render_to_response('reporting/form.html', {'message':e.message}, RequestContext(request))

        return render_to_response('reporting/form.html', {'message':'A moderator will review your report shortly. Thank you!'}, RequestContext(request))

#        if next:
#            return HttpResponseRedirect(next)
#        else:
#            return Http404
    else:
        return render_to_response('reporting/form.html', {'content_type':content_type, 'object_id':object_id, 'creator_field':creator_field, 'types':REPORT_TYPE}, RequestContext(request))
