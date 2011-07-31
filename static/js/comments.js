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
		parent.window.player['goto'](t);
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

var CommentImageFile = null;
function submitComment(){
	$('#submitbutton').attr("disabled", "true").css('color','#555').val('Posting...');
	if (CommentImageFile && ($('input[name=image]').val() == ''))
		postCommentImage();
	else
		postComment();
};

function postCommentImage(){
    $('#commentform').fileupload('send',{files: CommentImageFile});
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
    ctx.drawImage(image,
        0, 0, image.width*p, image.height,
        (canvas.width-w)/2, (canvas.height-h)/2, w*p, h
    );
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
    };
    reader.readAsDataURL(file);
    CommentImageFile = file;
}

var img, canvas;
function comment_onload() {
    canvas = $('canvas')[0];
	if (location.hash.substr(1)) hltag(location.hash.substr(1));
    
	//if (parent.window.reportpage) alert('iframed');

    $('#imagedropframe').click(function(e) {
        e.preventDefault();
        $('#imagefile').click();
    });

    $('#imagedropframe').bind('dragenter', function(){
        $('#imagedropframe').css('border','1px solid red');
    });
    $('#imagedropframe').bind('dragleave drop', function(){
        $('#imagedropframe').css('border','1px dashed black');
    });

    $('#commentform').fileupload({
        url: '/upload_image',
        dataType: 'json',
        'dropZone': $('#imagedropframe'),
        'fileInput': $('#imagefile'),
        add: function () { },
        'progress': function(e, data){
                var progress = parseInt(data.loaded / data.total * 100, 10);
                drawImageFit(canvas, img, progress);
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
                if (data.result.success) {
                    $('input[name=image]').val(data.result.value);
                    postComment();
                } else {
                    $('.errdiv').html('Error: '+data.result.error);
                }
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