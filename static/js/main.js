
var enablehover = false;
var hoverbound = false;
//document.domain = "localhost";

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

function indexLoad() {
	countdown();
	//alert($('#des').width());
	if ($('#des').height() < $('#des > div').height())
		$('#desexpand').show();
	$('#des').click(function(){ShowHideDescription();});
	$('.itemtags a').addClass('iframe');
	$('.iframe').fancybox(commentBox);
	if (commentsopen) {
		$('#commentcell').html(commentframe);
	} else {
		
	}
}

function countdown(){  
    //expiration = parseInt(Date.parse("Dec 21, 2012")/1000); //Test expiration  
	if (expiration == 0) return false;
    var now = new Date();  
    var current = parseInt(now.getTime()/1000);  
    var secs = expiration - current;
	if (secs < 0) secs = 0; //Stop negative countdown
    var hrs = parseInt(secs/(60*60));  
    secs -= hrs * 60 * 60;  
    var mins = parseInt(secs/(60));  
    secs -= mins * 60;
	$("#ctimer").html("<div>This page expires in:</div><div class=\"ctimertime\">" + hrs + "h " + mins + "m " + secs + "s</div>");
	if (expiration - current <= 0) return false;
	setTimeout("countdown()", 1000);
}

function IsNumeric(input){
   return (input - 0) == input && input.length > 0;
}

function ShowHideComments() {
	if (animating) return;
	if ($('#commentcell').css('display') == 'block') {
		animating = true;
		$('#sliderbutton div').removeClass().addClass('slideropen');
		$('#commentcell').animate({width:'0'},500,'swing');
		$('#itemcell').animate({right:'121px'},500,'swing',
				function(){
					$('#commentcell').css('display','none');
					SetCookieValue('CommentsClosed','on');
					animating = false;
				});
	} else {
		animating = true;
		$('#sliderbutton div').removeClass().addClass('sliderclose');
		$('#commentcell').css('display','block');
		$('#commentcell').animate({width:'430px'},500,'swing');
		$('#itemcell').animate({right:'550px'},500,'swing',
				function(){
					SetCookieValue('CommentsClosed','');
					animating = false;
//					if (!$('#comments')[0])
//						$('#commentcell').html(commentframe);
				});
	}
}

function ShowHideDescription() {
	if (animating) return;
	var h = ($('#des > div').height()+7) + 'px'; //7 = 5px padding-bottom + 1px border
	//alert($('#header').css('height')); return;
	if ($('#desexpand').hasClass('desexpandclose')) {
		animating = true;
		$('#desexpand').removeClass().addClass('desexpandopen');
		$('#des').animate({height:$('#headerindex').css('height')}, 300, 'swing',
				function(){ animating = false; });
	} else {
		animating = true;
		$('#desexpand').removeClass().addClass('desexpandclose');
		$('#des').animate({height:h},300,'swing',
				function(){ animating = false; });
	}	
}

function LoadBrowseFilter(){
	$('#content').load('browser/'+$('select[name=o]').val()+'/'+$('input[name=c]').val()+'/1');
}

function rateadex(score, item){
    //TODO: show loading icon
    $('#starset').attr('class','star-rating2');
    $('#starset li').attr('onclick','return false;');
//	$('#rated_text').load('../func/ajax.php?a=rate&i=' + item + '&v=' + rating + '&img=' + is_image,
//			function(data){
//				$('#current-rating').css('width',$('#rated_text #ratingval').html()+'%');
//			});
    $.post("/ajax/rate", {"id":item, "model":"adex", "score":score},
        function(data){
            if (data.success){

            } else {

            }
    }, "json");
}

function CloseAjaxDiv(obj){
    $(obj).slideUp('fast', function(){
        $(this).remove();
    });
    //alert($(obj).html());
}

function AddAjaxDiv(container, classname, msg){
    $(container).prepend('<div class="ajax_msg '+classname+'">'+msg+'<div onclick="CloseAjaxDiv(this.parentNode);" class="delicon"></div></div>');
}

function ShowHoverDiv(){
	$('#hoverdiv').css('visibility','visible');
}

function LoadHoverdiv(id, img, title, des, rating, comments, views, type, url, domain) {
	var imgclass;
	if ((rating == '') || (rating == 0)){
		rating = '0px';
	} else {
		rating = Math.round(((rating/5)*100)-1)+'%';
	}
	switch (type) {
	case '1': imgclass = 'videothumb'; break;
	case '2': case '3': imgclass = 'htmlthumb'; break;
	default: imgclass = '';
	}
	$('#hovertitle').html('<a href="'+url+'">'+title+'</a>');
	$('#imgdiv a').removeClass().addClass(imgclass).attr('href',url);
	$('#imgdiv span').removeClass().addClass('typeicon').addClass('icontype'+type);
	$('#imgdiv .topimg').attr('src', img);
	$('#hoverdiv .bottomimg').attr('src', (type==1)?img.substr(0,img.length-4):'');
	$('#hoverdescription').html(des);
	$('#hoverrating .current-rating').css('width',rating);
	//$('#hovercomments').html('<a href="http://'+domain+'/comments/'+id+'">'+comments+' Comment'+((comments==1)?'':'s')+'</a>');
	//$('#hoverviews').html('<a href="http://'+domain+'/data/'+id+'">'+views+' View'+((views==1)?'':'s')+'</a>');
	
	$('#hovercomments').html('<a class="buttonwrapper commentbutton iframe" href="http://'+domain+'/comments/'+id+'"><div class="buttonicon"></div><div class="buttoncount">'+comments+' Comment'+((comments==1)?'':'s')+'</div></a>');
	$('#hoverviews').html('<a class="buttonwrapper viewbutton iframe" href="http://'+domain+'/data/'+id+'"><div class="buttonicon"></div><div class="buttoncount">'+views+' View'+((views==1)?'':'s')+'</div></a>');
	$('#hoverdiv .iframe').fancybox(commentBox);
	ShowHoverDiv();
	enablehover = true;
}

function HideHoverdiv(){
	$('#hoverdiv').css('visibility','hidden');
	enablehover = false;
}

function SetCookieValue(name, value, domain){
	var expiration = new Date();
	expiration.setTime(expiration.getTime()+(3600*24*365*20));
	document.cookie = name+"="+value+"; expires="+expiration.toGMTString()+"; path=/;"+domain;
}

function SaveSettings(){
	var domain = $('#settings #domain').val();
	//var expiration = new Date();
	//expiration.setTime(expiration.getTime()+(3600*24*365*20));
	$('#settings input[type=checkbox]').each(function(index) {
		//alert(this.id+"="+(this.checked ? 'on' : '')+"; expires="+expiration.toGMTString()+"; path=/;"+domain);
		//document.cookie = this.id+"="+(this.checked ? 'on' : '')+"; expires="+expiration.toGMTString()+"; path=/;"+domain;
		SetCookieValue(this.id,(this.checked ? 'on' : ''));
	});
	alert('Settings Saved.');
}

var loginBox = {
	//'autoDimensions':	false,
    'type'          :   'iframe',
    'href'          :   '/login/?next=/login_redirect/',
	'width'			:	360,
	'height'		:	140,
	'padding'		:	10,
	'centerOnScroll':	true,
	'overlayColor'	:	'black',
	'overlayOpacity':	0.6,
	'onClosed'	    :	loginBoxOnClosed
};

function loginBoxOnClosed(){
    if ($('#userid').val()=='login')
        $('#userid').val('anon');
}

function LoginRedirect(username){
    parent.$('option[value=login]').val('name').html(username);
    parent.$('#loginmenu').html('<a href="/user/'+username+'">'+username+'</a> &middot; <a class="no-ajaxy" href="/logout/">logout</a>').ajaxify();
    parent.$.fancybox.close();
    parent.$.growlUI('Logged in. Welcome, '+username+'!');
}

function moveMouse(e){
	if (enablehover){
		var newY = e.pageY ? e.pageY : e.clientY + document.body.scrollTop + document.documentElement.scrollTop;
		newY = newY - 100;
		if (hoverbound) {
			var maxY = $(window).height() - $('#hoverdiv').height() - 22;
			var minY = 114;
			if (showads) maxY = maxY - 220;
			if (newY > maxY) newY = maxY;
			if (newY < minY) newY = minY;
		}
		//TODO: Snap hoverdiv to top of thumbs?
		//var changeY = Math.abs($('#hoverdiv').position().top - newY);
		//if (changeY > 40)
		//	$('#hoverdiv').stop().animate({top:newY+"px"}, changeY);
		//else
			$('#hoverdiv').css('top',newY+"px");
	}
}

function userid_load(){
    $("select#userid").change(function(){
        if ($(this).val() == "temp")
            $('input[name=name]').show('fast')
        else
            $('input[name=name]').hide('fast')

        if ($(this).val() == "login") {
            $.fancybox(loginBox);
        }
    });
}

function ajaxCSRF(){
    $(document).ajaxSend(function(event, xhr, settings) {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        function sameOrigin(url) {
            // url could be relative or scheme relative or absolute
            var host = document.location.host; // host + port
            var protocol = document.location.protocol;
            var sr_origin = '//' + host;
            var origin = protocol + sr_origin;
            // Allow absolute or scheme relative URLs to same origin
            return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
                (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
                // or any other URL that isn't scheme relative or absolute i.e relative.
                !(/^(\/\/|http:|https:).*/.test(url));
        }
        function safeMethod(method) {
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }

        if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    });
}

$(function(){
    $(document).mousemove(moveMouse);
    userid_load();
    $('#loginmenu .login').fancybox(loginBox);
    ajaxCSRF();
});
