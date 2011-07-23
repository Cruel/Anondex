var commentBox = {
	//'autoDimensions':	false,
	'width'			:	'90%',
	'height'		:	'90%',
	'padding'		:	0,
	'centerOnScroll':	true,
	'overlayColor'	:	'black',
	'overlayOpacity':	0.6
	//'onComplete'	:	reportWindowOnLoad	
};

function updateCharCount(src) {
	var charlimit = 500;
	if (src.value.length > charlimit)
		src.value = src.value.substring(0, charlimit);
	$('#charcounter').html('[Chars Left: ' + (charlimit - src.value.length) + ']');
};

function addtag(stag){
	var textarea = document.getElementById("comment");
	text = stag; //"[c]"+stag+"[/c]";
	if(textarea){
		if(textarea.createTextRange && textarea.caretPos){ // IE
			var caretPos=textarea.caretPos;
			caretPos.text=caretPos.text.charAt(caretPos.text.length-1)==" "?text+" ":text;
		}
		else if(textarea.setSelectionRange){ // Firefox
			var start=textarea.selectionStart;
			var end=textarea.selectionEnd;
			textarea.value=textarea.value.substr(0,start)+text+textarea.value.substr(end);
			textarea.setSelectionRange(start+text.length,start+text.length);
		}else{
			textarea.value+=text+" ";
		}
		textarea.focus();
	}
};

function reply(id){
	gotoDOM('.footerdiv');
	addtag('[c]'+id+'[/c]');
};

function vidseek(t) {
	//alert(t);
	if (parent.window.player)
		parent.window.player.goto(t);
	else
		alert('Video player not found.');
};

function rate(rating, item, is_image){
	$('#starset').attr('class','star-rating2');
	$('#starset li').attr('onclick','return false;'); //.click( function(){alert('ok'); return false;});
	$('#rated_text').load('../func/ajax.php?a=rate&i=' + item + '&v=' + rating + '&img=' + is_image,
			function(data){
				$('#current-rating').css('width',$('#rated_text #ratingval').html()+'%');
			});
};

function hltag(sTag){
	if (!$('#'+sTag).length) return true;
	$('.comment').removeClass('commentselected');
	$('#'+sTag).addClass('commentselected');
	//gotoDOM('a[name='+sTag+']');
	gotoDOM('#'+sTag);
	return false;
};

function gotoDOM(sDOM){
	//IE uses HTML tag for this... :/
	var offset = $(sDOM).offset();
	var scroll = ($('body').scrollTop() == 0) ? $('html').scrollTop() : $('body').scrollTop();
	var delay = Math.round(Math.abs(offset.top - scroll) / 4);
	//alert(delay);
	$('html, body').animate({scrollTop: offset.top}, delay);
};

function postComment(){
//    $('#commentform').ajaxSubmit({
//        dataType: 'json',
//        url: '/comments/post/',
//        //beforeSubmit: showRequest,
//        success: commentSuccess
//    });
	$.post('/comment/post/', $('#commentform').serialize(),
			function(data){
				if (data.success) {
					$('#submitbutton').val('Posted.');
                    $('.errdiv').html(data.html);
					alert('done. refreshing page...');
					//window.location.reload();
				} else {
                    alert('errors sent');
                    for (var error in data.errors)
					    $('.errdiv').append(error);
					$('#submitbutton').removeAttr("disabled").css('color','').val('Post Comment');
				}
			}
		);
};

function commentSuccess(data)  {
    if (data.success) {
        $('#submitbutton').val('Posted.');
        $('.errdiv').html(data.html);
        //window.location.reload();
    } else {
        for (var error in data.errors)
            $('.errdiv').append(error);
        $('#submitbutton').removeAttr("disabled").css('color','').val('Post Comment');
    }
};

var bUploadImage = false;
function submitComment(){
	$('#submitbutton').attr("disabled", "true").css('color','#555').val('Posting...');
	if (bUploadImage && ($('input[name=image]').val() == ''))
		postCommentImage();
	else
		postComment();
};

// Generate 32 char random uuid
var xid;
function gen_uuid() {
    var uuid = "";
    for (var i=0; i < 32; i++)
        uuid += Math.floor(Math.random() * 16).toString(16);
    return uuid;
};

function postCommentImage(){
    alert('uploading image...');
    $('#commentform').fileupload('send',{});
    return;
    $('#progressbar').css('visibility','visible');
    $('#progressbar').css('width',0);
    filename = $("#imglol").val().split(/[\/\\]/).pop();
	//alert('Uploading ' + filename + "...");
    xid = gen_uuid();
    //startProgressBarUpdate(xid);
    $('#commentform').ajaxSubmit({
        dataType: 'json',
        url: '/upload_image?x-id='+xid,
        //beforeSubmit: showRequest,
        success: imageSuccess
    });
};

function imageSuccess(data)  {
    if (data.success) {
        $('input[name=image]').val(data.value);
        postComment();
    } else {
        $('.errdiv').html('Error: '+data.error);
    }
};

function startProgressBarUpdate(upload_id) {
    $("#progressbar").fadeIn();
    $('#progressbar').css('visibility','visible');
    $('#progressbar').css('width',0);
    $('#progressbar').css('width',50+'%');
    if(g_progress_intv != 0)
        clearInterval(g_progress_intv);
    g_progress_intv = setInterval(function() {
        $.getJSON("/get_upload_progress?xid=" + upload_id, function(data) {
            if (data == null) {
                $('#progressbar').css('width','100%');
                clearInterval(g_progress_intv);
                g_progress_intv = 0;
                return;
            }
            var percentage = Math.floor(100 * parseInt(data.uploaded) / parseInt(data.length));
            //$("#progressbar").progressBar(percentage);
            $('#progressbar').css('width',percentage+'%');
        });
    }, 5000);
};

function drawImageFit(canvas, image, percentWidth){
    var p = typeof(percentWidth) != 'undefined' ? percentWidth/100 : 1;
    var ctx = canvas.getContext('2d');
    ratio = image.width / image.height;
    if (ratio >= 1){
        w = Math.min(image.width, canvas.width);
        h = w / ratio;
    } else {
        h = Math.min(image.height, canvas.height);
        w = h * ratio;
    }
    ctx.drawImage(image,0,0,image.width*p,image.height,0,0,w*p,h);
};

function loadImage(file){
    //var file = $('#imagefile')[0].files[0];
    var reader = new FileReader();
    reader.onload = function (event) {
        var ctx = canvas.getContext('2d');
        img = new Image();
        img.onload = function(){
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.globalAlpha = 0.5;
            drawImageFit(canvas, img);
            ctx.globalAlpha = 1.0;
            //drawImageFit(canvas, img, 50);
        }
        img.src = event.target.result;
        $('#imagedropframe').css('border','1px solid transparent');
    };
    reader.readAsDataURL(file);
    bUploadImage = true;
}

var img, canvas;
function comment_onload() {
    canvas = $('canvas')[0];
	if (location.hash.substr(1)) hltag(location.hash.substr(1));
	//if (parent.window.reportpage) alert('iframed');
	//loadImgUploader();

    $('#imagedropframe').click(function(e) {
        e.preventDefault();
        $('#imagefile').click();
    });

    $('#commentform').fileupload({
        url: '/upload_image',
        'dropZone': $('#imagedropframe'),
        'fileInput': $('#imagefile'),
        'progress': function(e, data){
                var progress = parseInt(data.loaded / data.total * 100, 10);
                drawImageFit(canvas, img, progress);
            },
        add: function (e, data) {

            },
        change: function (e, data) {
                loadImage(data.files[0]);
            },
        drop: function (e, data) {
                loadImage(data.files[0]);
//                $.each(data.files, function (index, file) {
//                    //alert('Dropped file: ' + file.name);
//                    loadImage(file);
//                });
            },
        done: function (e, data) {
                alert(data.result);
                alert(data.value);
            }
    });

	$('a.reply').each(function(i){
		if (!$($(this).attr('rel')).length) {
			//var hostdir = window.location.href;
			//var pos = hostdir.indexOf('/comments/');
			//if (pos < 0) pos = hostdir.indexOf('/image/');
			if (document.domain)
				$(this).attr('rel','http://'+document.domain+'/func/ajax.php?a=comment&i='+$(this).attr('rel').substring(1));
			//alert($(this).attr('rel'));
			$(this).cluetip({cluetipClass:'rounded', dropShadow:true, arrows:true, showTitle:false, fx:{open:'fadeIn',openSpeed:200}});
			$(this).addClass('iframe');
		} else
			$(this).cluetip({width:400, local:true, hideLocal:false, cluetipClass:'rounded', dropShadow:true, arrows:true, showTitle:false, fx:{open:'fadeIn',openSpeed:200}});
	});
	//$('.commentcontrols a').cluetip({positionBy:'bottomTop', splitTitle:'|', showTitle:false});
	parent.jQuery('a.iframe', window.document).fancybox(commentBox);
};