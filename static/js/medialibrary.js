
var THUMB_FRAME_COUNT = 5; // Must be same as in /medialibrary/utils.py
var attach_file_id = null;
var attach_file_html = null;
var attachBox = {
    'type'          :   'iframe',
    'href'          :   '/medialib/attach',
	'width'			:	700,
	'height'		:	400,
	'padding'		:	0,
	'centerOnScroll':	true,
	'overlayColor'	:	'black',
	'overlayOpacity':	0.6
};

function bindThumbEvents(selector){
    var config = {
        over: function(){videoThumbCycle(this)},
        timeout: 600, // milliseconds delay before onMouseOut
        out: function(){videoThumbCycle(null)}
    };
    $(selector+' .video').hoverIntent(config);
}

var cycleTimeout = null;
function videoThumbCycle(obj){
    if (obj==null) {
        clearTimeout(cycleTimeout);
    } else {
        position = parseInt($(obj).css('background-position').replace('%', ''));
        position = (position==100) ? 0 : position+25;
        $(obj).css('background-position', position+'%');
        cycleTimeout = setTimeout(function(){videoThumbCycle(obj);}, 500);
    }
}

function attachWindowOnClose(){
    //var obj = ($('#comments').length == 0) ? $(document).contents() : $('#comments').contents();
    if (attach_file_id == null){
        $('#fileselect').val('');
        //$('#attachpreview').hide('fast');
    } else {
        $('input[name=file]').val(attach_file_id);
        //$('#attachpreview').css('background-image','url('+parent.attach_file_html+')');
        $('#attachpreview').html(attach_file_html).show('fast');
    }
}

function addFromLibWindowOnClose(){
    if (attach_file_id != null){
        refreshFileList('add',attach_file_id);
    }
}

function medialib_onload(){
    $('.librarylist > div').click(function(){
        LibFileSelect(this);
    });
}

function LibFileSelect(obj){
    parent.attach_file_id = $(obj).data('id');
    parent.attach_file_html = $(obj).html();
    parent.$.fancybox.close();
}
