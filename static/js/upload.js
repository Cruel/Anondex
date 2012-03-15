var uploadBox = {
    'type'          :   'ajax',
    'href'          :   '/upload',
    'ajax':         {
                        dataFilter: function(data){
                            return $(data).find('#content').css({
                                'background-color':'#FDD',
                                'padding':'15px 0',
                                'width':'700px',
                                'border-radius':'5px'
                            });
                        }
                    },
    'padding'		:	0,
    'centerOnScroll':	true,
    'overlayColor'	:	'black',
    'overlayOpacity':	0.3,
    'afterShow'	    :	uploadBoxOnLoad
},
// Also see medialibrary/models.py constants
filetypes = {
    image: /^image\/(gif|jpeg|png)$/,
    audio: /^audio\/(mp3|mpeg|ogg|midi)$/,
    video: /^video\//,
    flash: /^application\/x-shockwave-flash$/
};

function uploadBoxOnLoad(){
    userid_load();
    //create_onload();
    upload_onload();
}

var drawfps = 24,
    framerate = 5100, // Should be a bit longer than ENCODE_PREVIEW_INTERVAL in medialibrary/utils.py
    drawstart = false,
    encodedrawing = null,
    framequeue = new Array();
function StartEncodeDrawing(){
    var ctx = uploadcanvas.getContext("2d"),
        time = +new Date(),
        timediff = (drawstart) ? (time-drawstart) : 0;
    if (!drawstart) drawstart = time;
    ctx.clearRect(0, 0, uploadcanvas.width, uploadcanvas.height);
    for (var i = 0; i < framequeue.length; ++i) {
        var frame = framequeue[i],
            new_x = uploadcanvas.width + (frame.width*i) - frame.width*(timediff/framerate);
        ctx.drawImage(frame, new_x, 0);
    }
    encodedrawing = setTimeout(StartEncodeDrawing, 1000/drawfps);
}

function StopEncodeDrawing(){
    clearTimeout(encodedrawing);
    drawstart = false;
}

function addFrameToQueue(jpeg_string){
    var frame = new Image();
    frame.src = "data:image/jpeg;base64,"+jpeg_string;
    frame.onload = function(){
        framequeue.push(this);
        if (uploadcanvas.height == 0) uploadcanvas.height = this.height;
    }
}

function drawb64jpeg(jpeg_string){
    var ctx = uploadcanvas.getContext("2d"),
    image = new Image();
    image.onload = function(){
        //canvas.width = image.width;
        canvas.height = image.height;
        ctx.drawImage(image, 0, 0);
    }
    image.src = "data:image/jpeg;base64,"+jpeg_string;
}

function showEncodeProgress(){
    $.get('/ajax/encode_progress', function(data){
        var progress = data.percent;
        if (progress < 100) {
            if (data.frame) addFrameToQueue(data.frame);
            if (!drawstart) StartEncodeDrawing();
            $("#upload-progress").progressbar({ value: progress });
            setTimeout(showEncodeProgress, 2000);
        } else {
            $("#upload-progress").progressbar('destroy');
            StopEncodeDrawing();
        }
    })
}

var filelist = new Array();
function startCreateUpload(){
    //first check for tags and TOS
    $('#upload-controller').block({message:'Uploading...'});
    $('#fileuploader').fileupload('option',{
        formData: {
            user: $('#userid_uploader').val(),
            tags: $('#upload-taglist').tagHandler('getSerializedTags')
        }
    });
    for (i in filelist)
        $('#fileuploader').fileupload('send',{files: filelist[i]});
}

function loadUploader(){
    $(document).bind('drop dragover', function (e) {
        e.preventDefault(); // Prevent browser's default action
    });

    $(document).bind('dragover', function (e) {
        var dropZone = $('#upload-controller'),
            timeout = window.dropZoneTimeout;
        if (!timeout) {
            dropZone.addClass('in');
        } else {
            clearTimeout(timeout);
        }
        if (e.target === dropZone[0]) {
            dropZone.addClass('hover');
        } else {
            dropZone.removeClass('hover');
        }
        window.dropZoneTimeout = setTimeout(function () {
            window.dropZoneTimeout = null;
            dropZone.removeClass('in hover');
        }, 100);
    });

    $('#fileuploader').fileupload({
        url: '/upload_file',
        dataType: 'json',
        'dropZone': $('#upload-controller'),
        //'fileInput': $('#file'),
        sequentialUploads: true,
        maxFileSize: 50000,
        add: function (e, data) {
                 $.each(data.files, function (index, file) {
                    var duplicate = false;
                    for (i in filelist)
                        if (filelist[i].name == file.name)
                            duplicate = true;
                    if (!duplicate){
                        filelist.push(file);
                        if (filetypes.image.test(file.type)) {
                            $('#filelisttest').append('<li>'+file.name+' - '+file.type+'</li>');
                            //alert('image added');
                        } else if (filetypes.video.test(file.type)) {
                            if (filelist.length > 1){
                                filelist.pop();
                                alert("Videos cannot be bundled with other files.\nYou must upload videos by themselves by removing other files in queue.");
                            } else {
                                //alert('video added');
                                $('#filelisttest').append('<li>'+file.name+' - '+file.type+'</li>');
                            }
                        } else if (filetypes.audio.test(file.type)) {
                            $('#filelisttest').append('<li>'+file.name+' - '+file.type+'</li>');
                            //alert ('audio added');
                        } else if (filetypes.flash.test(file.type)) {
                            if (filelist.length > 1){
                                filelist.pop();
                                alert("Flash files cannot be bundled with other files.\nYou must upload flash files by themselves by removing other files in queue.");
                            } else {
                                //alert('flash added');
                                $('#filelisttest').append('<li>'+file.name+' - '+file.type+'</li>');
                            }
                        } else{
                            filelist.pop();
                            alert('The file type ('+file.type+') is not supported.');
                        }
                    }
                });
//            alert(filelist.length);
//            $('#upload-controller').blockEx();
//            data.submit();
        },
        'progress': function(e, data){
            var progress = parseInt(data.loaded / data.total * 100, 10);
            //drawImageFit(canvas, img, progress);
            if (progress == 100){
                if (filetypes.video.test(data.files[0].type)){
                    $('#upload-controller').block({message:'Encoding video...'});
                    setTimeout(showEncodeProgress, 3000);
                }
            }
            //$('#events').append('<p>'+progress+'-'+data.files[0].name+'</p>');
            $("#upload-progress").progressbar({
                value: progress
            });
        },
        change: function (e, data) {
            //loadImage(data.files[0]);
        },
        drop: function (e, data) {
            //loadImage(data.files[0]);
            $.each(data.files, function (index, file) {
                //alert('Dropped file: ' + file.name);
                //loadImage(file);
            });
        },
        done: function (e, data) {
            $("#upload-progress").progressbar("destroy");
            $('#upload-controller').unblock();
            filelist = new Array();
            if (data.result.success) {
                if($('.fancybox-opened').length) {
                    refreshFileList('add',data.result.id);
                    $.fancybox.close();
                }
                //$.growlUI('Successfully uploaded '+data.files[0].name+'!');
                AddAjaxDiv('#uploadresults', "ajax_msg_success", 'Successfully uploaded: <input type="text" value="'+data.result.url+'" onclick="this.select();" />');
            } else {
                AddAjaxDiv('#uploadresults', "ajax_msg_error", data.result.error);
            }
        }
    });
}

var uploadcanvas;
function upload_onload(){
    uploadcanvas = $("#uploadcanvas")[0]
    loadUploader();
    userid_load("userid_uploader");
    $('#upload-controller').click(function(e) {
        $('#file').click();
    });
//    $('#upload-taglist').tagHandler({
//        getURL: '/ajax/taglist',
//        autocomplete: true
//    });
    loadTagHandler('upload-taglist');
    loadTagHandler('upload-taglist');
}