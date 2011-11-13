import random
import string
from adex.models import Adex
import simplejson as json

def processCreateVars(vars):
    errors = list()
    for i in vars.keys():
        if vars[i] == 'undefined': vars[i] = ''
    vars['type'] = int(vars.get('type'))
    if not vars.get('title'): errors.append('"Title" must be defined.')
    if not vars.get('description'): errors.append('"Description" must be defined.')
    if not vars.get('tags'): errors.append('You must supply some tags.')
    if not vars.get('name'):
        pass # check name availability
    if vars.get('type') == 0:
        if not vars.get('imgtemplate'): errors.append('You must select an image template layout.')
        if not vars.get('imageselect'): errors.append('You must upload an image.')
    elif vars.get('type') == 1:
        if not vars.get('videoselect'): errors.append('You must upload an image.')
    elif vars.get('type') == 2:
        if not vars.get('flashselect'): errors.append('You must upload a flash (.swf) file.')
    elif vars.get('type') == 3:
        if not vars.get('url'): errors.append('You must define a URL.')
    elif vars.get('type') == 4:
        if not vars.get('htmlselect') and not vars.get('html'):
            errors.append('You must upload an HTML file, or input custom HTML.')
    else:
        errors.append('You must select a template.')
    if vars.get('preview') == '0' and not vars.get('recaptcha_response_field'):
        errors.append('Captcha must be completed.')
    # TODO: More checks... for valid files, valid url, etc... ?
    return errors if len(errors) > 0 else False


def genItemCode():
    chars = string.letters + string.digits
    ret = ''.join(random.choice(chars) for i in range(3))
    try:
        Adex.objects.get(item_code=ret)
        return genItemCode()
    except Adex.DoesNotExist:
        return ret


# {"image":{"style":"stretch","proportional":true},"audio":null}
def genData(vars):
    #ret = {"image":{"style":"stretch","proportional":True},"audio":None}
    ret = {}
    media = []
    if vars['type'] == 0:
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
    elif vars['type'] == 1:
        ret = {'video':{'id':int(vars['videoselect'])}}
        media = [ret['video']['id']]
    elif vars['type'] == 2:
        ret = {'flash':{'id':int(vars['flashselect'])}}
        media = [ret['flash']['id']]
    elif vars['type'] == 3:
        ret = {'url':vars['url']}

    return json.dumps(ret), media