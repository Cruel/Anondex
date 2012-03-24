var filelist = [], imagelist = [],
uploadBox = {
    'type'          :   'ajax',
    'href'          :   '/upload',
    'padding'		:	0,
    'centerOnScroll':	true,
    'overlayColor'	:	'black',
    'overlayOpacity':	0.3,
    'ajax':         {
                        dataFilter: function(data){
                            return $(data).find('#content').css({
                                'background-color':'#FDD',
                                'padding':'15px 0',
                                'width':'684px',
                                'border-radius':'5px'
                            });
                        }
                    },
    'afterShow'	    :	function(){
                            userid_load();
                            //create_onload();
                            upload_onload();
                            filelist = [];
                        },
    'afterClose'    :   function(){
                            if ($('#comment').length && ($('input[name=file]').val() == "")){
                                $('#fileselect').val('');
                            }
                        }
},
// Also see medialibrary/models.py constants
filetypes = {
    image: /^image\/(gif|jpeg|png)$/,
    audio: /^audio\/(mp3|mpeg|ogg|midi)$/,
    video: /^video\//,
    flash: /^application\/x-shockwave-flash$/
};

// Video encoding preview stream
var drawfps = 24,
    framerate = 5100, // Should be a bit longer than ENCODE_PREVIEW_INTERVAL in medialibrary/utils.py
    drawstart = false,
    encodedrawing = null,
    framequeue = [];
function StartEncodeDrawing(){
    var time = +new Date(),
        timediff = (drawstart) ? (time-drawstart) : 0;
    if (!drawstart) drawstart = time;
    uploadctx.clearRect(0, 0, uploadcanvas.width, uploadcanvas.height);
    for (var i = 0; i < framequeue.length; ++i) {
        var frame = framequeue[i],
            new_x = uploadcanvas.width + (frame.width*i) - frame.width*(timediff/framerate);
        uploadctx.drawImage(frame, new_x, 0);
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

function addFileToList(file){
    var image = new Image();
    var reader = new FileReader();
    reader.onload = function (e) {
        image.src = e.target.result;
    };
    image.onload = function(){
        addImageToList(this);
    };
    reader.readAsDataURL(file);
}

function addImageToList(image){
    var ratio = image.width/image.height;
    imagelist.push({
        width   : ratio*100,
        image   : image
    });
    if (imagelist.length == filelist.length)
        drawImageList();
}

function reloadFileList(){
    $('#filelisttest').html('');
    imagelist = []
    for (i in filelist){
        var file = filelist[i];
        //$('#filelisttest').append('<li>'+file.name+' - '+file.type+'</li>');
        if (filetypes.image.test(file.type)){
            addFileToList(file);
        } else {
            $('#filelisttest').html('<li>'+file.name+' - '+file.type+'</li>');
            var img = new Image();
            img.onload = function(){ addImageToList(this); }
            img.src = 'http://localhost/media/audio.jpg';
        }
    }
    $('#canvasdiv').show('fast');
}

var ok = 0;
function progresstest(){
    ok += 0.01;
    canvasprogress(ok);
    if (ok <= 1.0)
        setTimeout(progresstest, 30);
}

function canvasprogress(p){
    var width = 0;
    for (i in imagelist)
        width += imagelist[i].width;
    width = Math.max(width, uploadcanvas.width);
    drawImageList((uploadcanvas.width-width)*p,p);
}

function onCanvasMouseMove(e){
    var w       = $(this).width(),
        edge    = w * 0.1,
        new_w   = w - (edge*2),
        curX    = e.pageX - $(this).offset().left - edge;
    curX = Math.max(curX, 0);
    curX = Math.min(curX, new_w);
    var pos = curX / new_w;
    //$("#filelisttest").html(e.data.width + " - " + $(this).offset().left + " - " + curX);
    drawImageList(-pos*(e.data.width - w));
}

function drawImageList(offset, percent){
    if (typeof(offset) == 'undefined') offset = 0;
    if (typeof(percent) == 'undefined') percent = false;
    var x = 0;
    clearUploadCanvas();
    uploadctx.globalAlpha = (percent === false) ? 1.0 : 0.4;
    for (i in imagelist){
        var img = imagelist[i];
        if ((x+offset < uploadcanvas.width) && (x+offset > -img.width))
            uploadctx.drawImage(img.image, x+offset, 0, img.width, 100);
        x += img.width;
    }
    uploadctx.globalAlpha = 1.0;
    $("#uploadcanvas").unbind('mousemove');
    if (percent === false) {
        if (x > uploadcanvas.width){
            $("#uploadcanvas").mousemove({width:x}, onCanvasMouseMove);
        }
    } else {
        var percent_w = x * percent;
        x = 0;
        for (i in imagelist){
            var img = imagelist[i];
            if (percent_w-img.width < 0) {
                uploadctx.drawImage(img.image, 0, 0, img.image.width*(percent_w/img.width), img.image.height, x+offset, 0, percent_w, 100);
                break;
            } else
                uploadctx.drawImage(img.image, x+offset, 0, img.width, 100);
            percent_w -= img.width;
            x += img.width;
        }
    }
}

function startCreateUpload(){
    var data = {
        title: $('#filetitle').val(),
        user : $('#userid_uploader').val(),
        tags : $('#upload-taglist').tagHandler('getSerializedTags'),
        tos  : $("#upload-tos").is(':checked')
    }
    if (!IsDefined(data.tags)) { alert('Uploaded files must be tagged.'); return; }
    if (!verifyTags(data.tags)) return;
    if (!data.tos) { alert('You must agree to the Terms of Service before uploading content.'); return; }
    $('#upload-controller').block({message:'Uploading...'});
    $('#fileuploader').fileupload('option',{
        formData: data
    });
//    for (i in filelist)
//        $('#fileuploader').fileupload('send',{files: filelist[i]});
    $('#fileuploader').fileupload('send',{files: filelist});
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
        //sequentialUploads: true,
        singleFileUploads: false,
        maxFileSize: 50000,
        add: function (e, data) {
                 $.each(data.files, function (index, file) {
                    if (filelist.length > 0 && ((!filetypes.image.test(file.type)) || (!filetypes.image.test(filelist[filelist.length-1].type)))) {
                        filelist = [];
                    }
                    var duplicate = false;
                    for (i in filelist)
                        if (filelist[i].name == file.name)
                            duplicate = true;
                    if (!duplicate){
                        filelist.push(file);
                        for (i in filetypes)
                            if (filetypes[i].test(file.type))
                                return 1; // Continue to next iteration
                        filelist.pop();
                        alert('The file type ('+file.type+') is not supported.');
                    }
                });
//            $('#upload-controller').blockEx();
//            data.submit();
            reloadFileList();
        },
        'progress': function(e, data){
            var progress = parseInt(data.loaded / data.total * 100, 10);
            if (progress == 100){
                if (filetypes.video.test(data.files[0].type)){
                    $('#upload-controller').block({message:'Encoding video...'});
                    setTimeout(showEncodeProgress, 3000);
                }
            }
            $("#upload-progress").progressbar({
                value: progress
            });
            //console.log("Progess: "+progress)
            canvasprogress(progress/100);
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
            if (data.result.success) {

                if ($('.fancybox-opened').length) {
                    if ($('#comment').length){
                        $('input[name=file]').val(data.result.id);
                        $('#attachpreview').html(data.result.thumb).show('fast');
                    } else {
                        refreshFileList('add',data.result.id);
                    }
                    $.fancybox.close();
                }
                //$.growlUI('Successfully uploaded '+data.files[0].name+'!');
                resetUploadForm();
                AddAjaxDiv('#uploadresults', "ajax_msg_success", 'Successfully uploaded: <input type="text" value="'+data.result.url+'" onclick="this.select();" />');
            } else {
                AddAjaxDiv('#uploadresults', "ajax_msg_error", data.result.error);
            }
        }
    });
}

function clearUploadCanvas(){ uploadctx.clearRect(0, 0, uploadcanvas.width, uploadcanvas.height); }

function resetUploadForm(){
    filelist = [];
    loadTagHandler('upload-taglist');
    $('#filetitle').val('');
    clearUploadCanvas();
    $('#canvasdiv').hide('fast');
}

var uploadcanvas, uploadctx;
function upload_onload(){
    uploadcanvas = $("#uploadcanvas")[0]
    uploadctx = uploadcanvas.getContext('2d');
    loadUploader();
    userid_load("userid_uploader");
    $('#upload-controller').click(function(e) { $('#file').click(); });
    loadTagHandler('upload-taglist');
}