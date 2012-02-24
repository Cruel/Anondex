import Image as pil
import base64
import os
import subprocess, re
from django.core.cache import cache
from pyvirtualdisplay import Display
from selenium import webdriver
import time
from medialibrary.video_encoder import VideoEncoder
from medialibrary.video_inspector import VideoInspector

#video_size_pattern = re.compile(r'Stream.*Video.* ([0-9]{2,4})x([0-9]{2,4})')
#media_duration_pattern = re.compile(r'Duration: *([0-9]{2,}):([0-9]{2,}):([0-9]{2,}).')
from settings import MEDIA_ROOT

LIBRARYFILE_THUMB_WIDTH = 150
LIBRARYFILE_THUMB_HEIGHT = 112
LIBRARYFILE_THUMB_RATIO = float(LIBRARYFILE_THUMB_WIDTH) / float(LIBRARYFILE_THUMB_HEIGHT)

THUMB_FRAME_COUNT = 5 # Must be save as in medialibrary.js
JPEG_QUALITY = 8 # From 0-10

ENCODE_PREVIEW_INTERVAL = 5.000


def get_video_size(videofile):
    video = VideoInspector(videofile)
    #print video.width(), video.height()
    return video.width(), video.height()

def get_media_duration(mediafile):
    video = VideoInspector(mediafile)
    return video.duration() / 1000

def base64Encode(image_file):
    #return 'jpg1_b64 = \\\n"""' + base64.encodestring(open(image_file,"rb").read()) + '"""'
    return base64.b64encode(open(image_file,"rb").read())

def encodeVideo(video_input, video_output, ip):
    encodeVideo.encode_time = 0

    def encode_progress(current_pos, duration):
        percent = int((current_pos/duration)*100)
        cache.set('%s_encode'%ip, percent, 15)
        if encodeVideo.encode_time < time.time():
            encodeVideo.encode_time = time.time() + ENCODE_PREVIEW_INTERVAL
            encode_preview(percent)

    def encode_preview(percent):
        framefile = '%s.jpg'%video_input
        os.system('ffmpegthumbnailer -i %s -o %s -t %d%% -q %d -s %d' % (video_input, framefile, percent, JPEG_QUALITY, 150))
        print "frame %d" % percent
        cache.set('%s_frame'%ip, base64Encode(framefile), 15)

    if cache.get('%s_encode'%ip):
        print "Already encoding a video!"
    video = VideoEncoder(video_input)
    print "Video input:", video_input
    print "Video output:", video_output
    video.execute(
        "%(ffmpeg_bin)s -y -i %(input_file)s -vcodec libx264 -vpre medium %(output_file)s",
        video_output,
        encode_progress
    )
    cache.set('%s_encode'%ip, 100, 15)
    print "encoding done"

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
        # Example: ffmpegthumbnailer -o test.jpg -t 100% -q 8 -s 250 -i adex28_ticklefest.flv.mp4
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
        time.sleep(5)
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