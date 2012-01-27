import Image as pil
import os
import subprocess, re
from pyvirtualdisplay import Display
from selenium import webdriver
import time

video_size_pattern = re.compile(r'Stream.*Video.* ([0-9]{2,4})x([0-9]{2,4})')
media_duration_pattern = re.compile(r'Duration: *([0-9]{2,}):([0-9]{2,}):([0-9]{2,}).')

LIBRARYFILE_THUMB_WIDTH = 150
LIBRARYFILE_THUMB_HEIGHT = 112
LIBRARYFILE_THUMB_RATIO = float(LIBRARYFILE_THUMB_WIDTH) / float(LIBRARYFILE_THUMB_HEIGHT)

THUMB_FRAME_COUNT = 5 # Must be save as in medialibrary.js
JPEG_QUALITY = 8 # From 0-10

def get_video_size(videofile):
    p = subprocess.Popen(['ffmpeg', '-i', videofile], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    match = video_size_pattern.search(stderr)
    if match:
        x, y = map(int, match.groups()[0:2])
    else:
        x = y = 0
    return x, y


def get_media_duration(mediafile):
    p = subprocess.Popen(['ffmpeg', '-i', mediafile], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    match = media_duration_pattern.search(stderr)
    if match:
        hours, minutes, seconds = map(int, match.groups()[0:3])
    else:
        return 0
    return hours*60*60 + minutes*60 + seconds


def genVideoThumb(videofile, imagefile):
    (width, height) = get_video_size(videofile)
    frame_step = int(100/THUMB_FRAME_COUNT)
    ratio = float(width) / float(height)
    if width > LIBRARYFILE_THUMB_WIDTH:
        width = LIBRARYFILE_THUMB_WIDTH
        height = int(width / ratio)
    if height > LIBRARYFILE_THUMB_HEIGHT:
        height = LIBRARYFILE_THUMB_HEIGHT
        width = int(height * ratio)
    width_offset = (LIBRARYFILE_THUMB_WIDTH-width)/2
    height_offset = int((LIBRARYFILE_THUMB_HEIGHT-height)/2)
    new_image = pil.new("RGB", (LIBRARYFILE_THUMB_WIDTH*THUMB_FRAME_COUNT, LIBRARYFILE_THUMB_HEIGHT))
    for i in range(THUMB_FRAME_COUNT):
        framefile = '%s%d.jpg' % (imagefile, i)
        # TODO: fix keyframing issue (perhaps flvtool2?)
        os.system('ffmpegthumbnailer -i %s -o %s -t %d%% -q %d -s %d' % (videofile, framefile, i*frame_step, JPEG_QUALITY, width))
        img = pil.open(framefile)
        new_image.paste(img, (LIBRARYFILE_THUMB_WIDTH*i+width_offset, height_offset))
        os.remove(framefile)
    new_image.save(imagefile)
    return True


def webthumb(url, filename, is_flash=False):
    script = '''
        var s = document.createElement('script');
        s.src = 'http://cruels.net/sb/flashfix.js';
        document.body.appendChild(s);
    '''
    print "webthumb(%s, %s)" % (url, filename)
    display = Display(visible=0, size=(1200, 900))
    display.start()
    browser = webdriver.Firefox()
    browser.get(url)
    if is_flash:
        time.sleep(1)
    else:
        browser.execute_script(script)
        time.sleep(6)
    tmpfile = '%s.tmp' % filename
    browser.get_screenshot_as_file(tmpfile)
    img = pil.open(tmpfile)
    width, height = img.size
    if is_flash:
        resized = img.resize((LIBRARYFILE_THUMB_WIDTH,LIBRARYFILE_THUMB_HEIGHT), pil.ANTIALIAS)
    else:
        ratio = float(width) / float(height)
        resized = img.resize((LIBRARYFILE_THUMB_WIDTH,int(LIBRARYFILE_THUMB_WIDTH/ratio)), pil.ANTIALIAS)
    resized.save(filename)
    os.remove(tmpfile)
    print "Saved %s." % filename
    browser.quit()
    display.stop()
    return True