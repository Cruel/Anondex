from PIL import Image as pil
from os.path import basename
from django.core.files.move import file_move_safe
from comments.utils import md5_file
from medialibrary.models import LibraryFile
import settings

def ProcessLibraryImage(tmpfile):
    filename = basename(tmpfile)
    im = pil.open(tmpfile)
    (width, height) = im.size
    md5 = md5_file(tmpfile)
    # If image md5 doesn't already exist, make the image
    try:
        file = LibraryFile.objects.get(md5=md5)
    except LibraryFile.DoesNotExist:
        file = LibraryFile(type=1, width=width, height=width, md5=md5, name=filename)
        file.save()
        im.thumbnail((100,100), pil.ANTIALIAS)
        file.filename = "adex%s_%s" % (file.id, filename)
        im.save(settings.MEDIA_ROOT + "i/thumb/%s" % file.filename)
        file_move_safe(tmpfile, settings.MEDIA_ROOT + "i/%s" % file.filename)
        file.save()
    return file.id