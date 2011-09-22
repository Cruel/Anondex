
var THUMB_FRAME_COUNT = 5 // Must be same as in /medialibrary/utils.py
var attach_file_id = null;
var attach_file_thumb = null;
var attachBox = {
    'type'          :   'iframe',
    'href'          :   '/lib/attach',
	'width'			:	600,
	'height'		:	400,
	'padding'		:	0,
	'centerOnScroll':	true,
	'overlayColor'	:	'black',
	'overlayOpacity':	0.6,
	'onClosed'	    :	attachWindowOnClose
};

function attachWindowOnClose(){
    if (attach_file_id == null){
        $('#fileselect').val('');
    } else {
        $('input[name=file]').val(attach_file_id);
        $('#attachpreview').css('background-image','url('+attach_file_thumb+')');
        $('#attachpreview').show('fast');
    }
}

function medialib_onload(){
    $('#librarylist > div').click(function(){
        LibFileSelect(this);
    });
}

function LibFileSelect(obj){
    parent.attach_file_id = $(obj).data('id');
    parent.attach_file_thumb = $(obj).data('thumburl');
    parent.$.fancybox.close();
}