
var currentpage="home.php";
//var changeinprogress = false;
var enablehover = false;
var hoverbound = false;
document.domain = "localhost:8000";

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
};

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
};

function fadeScale(objselector){
	$(objselector+' > *').not("script").fadeTo(0,0);
	$(objselector).css('visibility','visible');
	$(objselector+' > *').not("script").delay(200).each(function(index) {
		$(this).delay(index*70).fadeTo(500,1);
	});
};

function IsNumeric(input){
   return (input - 0) == input && input.length > 0;
};

function ratecomment(id, rating){
	$('#'+id+' .commentrating').load('../func/ajax.php?a=ratecomment&i='+id+'&r='+rating);
};

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
					if (!$('#comments')[0])
						$('#commentcell').html(commentframe);
				});
	}
};

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
};

function LoadPage(tid, page){
	if (currentpage == page) return false;
	$('#content').load(page, function(){create_onload();});
	$('#menu li').removeClass('active');
	$(tid).parent().addClass('active');
	currentpage = page;
};

function LoadBrowseFilter(){
	$('#content').load('browser/'+$('select[name=o]').val()+'/'+$('input[name=c]').val()+'/1');
};

function rate(rating, item, is_image){
	$('#starset').attr('class','star-rating2');
	$('#starset li').attr('onclick','return false;'); //.click( function(){alert('ok'); return false;});
	$('#rated_text').load('../func/ajax.php?a=rate&i=' + item + '&v=' + rating + '&img=' + is_image,
			function(data){
				$('#current-rating').css('width',$('#rated_text #ratingval').html()+'%');
			});
}

function CloseAjaxDiv(obj){
    $(obj).remove();
    alert($(obj).html());
}

function AddErrorDiv(container, msg){
    $(container).prepend('<div class="error_ajax">Error: '+msg+' <a href="#" onclick="CloseAjaxDiv(this.parentNode); return false;">Close</a></div>');
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
	
function do_onload(){
    /*
	var page = location.hash.substr(1);
	if (page == '') page = 'home';
	arrpage = page.split('/');
	LoadPage($('#link'+arrpage[0]), ((arrpage[0]=='browser')? page : 'pages/'+page+'.php'));
	*/
}

$(function(){$(document).mousemove(moveMouse);});
