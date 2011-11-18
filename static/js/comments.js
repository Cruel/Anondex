
function ratecomment(score, item){
    //TODO: show loading icon
    var upvote = "#"+item+" .upvote"
    var downvote = "#"+item+" .downvote"
    $(downvote+","+upvote).attr('onclick','').removeClass('voted');
    if (score=='2') $(upvote).addClass('voted');
    if (score=='1') $("#"+item+" .downvote").addClass('voted');
    $.post("/ajax/rate", {"id":item, "model":"adexcomment", "score":score},
        function(data){
            if (data.success){
                if (score=='2' || score=='0')
                    $(downvote).attr('onclick',"ratecomment('1','"+item+"');");
                if (score=='1' || score=='0')
                    $(upvote).attr('onclick',"ratecomment('2','"+item+"');");
                if (score=='2')
                    $(upvote).attr('onclick',"ratecomment('0','"+item+"');");
                if (score=='1')
                    $(downvote).attr('onclick',"ratecomment('0','"+item+"');");
                $("#"+item+" .commentrating").html((data.rating==0)?'':data.rating).css('color',(data.rating>0)?'green':'red');
            } else {
                $(downvote).attr('onclick',"ratecomment('1','"+item+"');").removeClass('voted');
                $(upvote).attr('onclick',"ratecomment('2','"+item+"');").removeClass('voted');
                if (data.value=="You must be logged in to vote.") {
                    $.fancybox(loginBox);
                } else {
                    alert(data.value);
                }
            }
    }, "json");
}

function updateCharCount(src) {
	var charlimit = 500;
	if (src.value.length > charlimit)
		src.value = src.value.substring(0, charlimit);
	$('#charcounter').html('[Chars Left: ' + (charlimit - src.value.length) + ']');
}

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
}

function reply(id){
	gotoDOM('.footerdiv');
	addtag('[c]'+id+'[/c]');
}

function vidseek(t) {
	//alert(t);
	if (parent.window.player)
		parent.window.player['goto'](t);
	else
		alert('Video player not found.');
}

function hltag(sTag){
	if (!$('#'+sTag).length) return true;
	$('.comment').removeClass('commentselected');
	$('#'+sTag).addClass('commentselected');
	//gotoDOM('a[name='+sTag+']');
	gotoDOM('#'+sTag);
	return false;
}

function gotoDOM(sDOM){
	//IE uses HTML tag for this... :/
	var offset = $(sDOM).offset();
	var scroll = ($('body').scrollTop() == 0) ? $('html').scrollTop() : $('body').scrollTop();
	var delay = Math.round(Math.abs(offset.top - scroll) / 4);
	//alert(delay);
	$('html, body').animate({scrollTop: offset.top}, delay);
}

function postComment(){
	$.post('/comment/post/', $('#commentform').serialize(),
			function(data){
                $("#commentformdiv").unblock();
				if (data.success) {
					$('#submitbutton').val('Posted.');
                    $('#newcomment').html(data.html);
                    $.growlUI('Comment Posted.');
				} else {
                    //alert('errors sent');
                    for (var error in data.errors)
					    //$('.errdiv').append(error);
                        AddAjaxDiv('.errdiv', 'ajax_msg_error', 'Error: '+error);
					$('#submitbutton').removeAttr("disabled").css('color','').val('Post Comment');
				}
        }, "json" );
}

var CommentImageFile = null;
function submitComment(){
	$('#submitbutton').attr("disabled", "disabled").css('color','#555').val('Posting...');
	if (CommentImageFile && ($('input[name=file]').val() == ''))
		postCommentImage();
	else
		postComment();
}

function postCommentImage(){
    $('#commentform').fileupload('send',{files: CommentImageFile});
}

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
}

function loadImage(file){
    if (file != null)
        $('#attachpreview').show('fast');
    else
        canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height);
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

function comment_cluetips(){
	$('a.reply').each(function(i){
        if (!$(this).hasClass('cluetiplink')) {
            if (!$($(this).attr('rel')).length) {
                //if (document.domain)
                    $(this).attr('rel','/ajax/comment/'+$(this).attr('rel').substring(1));
                //alert($(this).attr('rel'));
                $(this).cluetip({cluetipClass:'rounded', dropShadow:true, arrows:true, showTitle:false, fx:{open:'fadeIn',openSpeed:200}});
                //$(this).addClass('iframe');
                $(this).addClass('cluetiplink');

            } else
                $(this).cluetip({width:400, local:true, hideLocal:false, cluetipClass:'rounded', dropShadow:true, arrows:true, showTitle:false, fx:{open:'fadeIn',openSpeed:200}});
        }
    });
	//$('.commentcontrols a').cluetip({positionBy:'bottomTop', splitTitle:'|', showTitle:false});
	//parent.jQuery('a.iframe', window.document).fancybox(commentBox);
}

var img, canvas;
function comment_onload() {
    canvas = $('canvas')[0];
	if (location.hash.substr(1)) hltag(location.hash.substr(1));

    $('#submitbutton').click(function(){
        $("#commentformdiv").blockEx();
        $('.errdiv *').slideUp('fast');
        submitComment();
    });

    $("#fileselect").change(function(){
        loadImage(null);
        $('input[name=file]').val('');
        $('#attachpreview').css('background-image','');
        $("#imagefile").replaceWith('<input type="file" name="imagefile" id="imagefile" accept="image/png,image/jpeg,image/gif" />');
        CommentImageFile = null;
        $('#commentform').fileupload('option', 'fileInput', $('#imagefile'));
        $('#attachpreview').hide('fast').unbind('click');
        if ($(this).val() == "upload"){
            $("#attachpreview").click(function(){
                $('#imagefile').click();
            });

        }
        if ($(this).val() == "library"){
            $("#attachpreview").click(function(){
                attachBox.onClosed = attachWindowOnClose;
                parent.$.fancybox(attachBox);
            });

        }
        $("#attachpreview").click();
    });


    
	//if (parent.window.reportpage) alert('iframed');

//    $('#imagedropframe').click(function(e) {
//        e.preventDefault();
//        $('#imagefile').click();
//    });

    $('.formtable').bind('dragenter', function(){
        $(this).css('border','1px solid red');
    });
    $('.formtable').bind('dragleave drop', function(){
        $(this).css('border','1px dashed black');
    });

    $('#commentform').fileupload({
        url: '/upload_image',
        dataType: 'json',
        'dropZone': $('.formtable'),
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
                    $('input[name=file]').val(data.result.value);
                    postComment();
                } else {
                    AddAjaxDiv('.errdiv', 'ajax_msg_error', 'Error: '+data.result.error);
                    $('#submitbutton').removeAttr("disabled").css('color','').val('Post Comment');
                }
            }
    });

    comment_cluetips();

};