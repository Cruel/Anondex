var reportSettings = {
	//'autoDimensions':	false,
	//'width'			:	350,
	//'height'		:	200,
	'padding'		:	25,
	'overlayColor'	:	'black',
	'modal'			:	true,
	'overlayOpacity':	0.6,
	'onComplete'	:	reportWindowOnLoad	
};

function closeReportWindow() {
	$('.reportwindow').remove();
};

function reportSubmit() {
	$.post(reportpage, {'type':$('.reportselect').val(), 'other':$('.reporttext').val()},
			function(data){
				$.fancybox(data,reportSettings);
			});
};

function reportWindowOnLoad(){
	$('.reportcancel').click(function(){
		$.fancybox.close();
	});
	$('.reportsubmit').click(reportSubmit);
	$('.reportselect').change(function(){
		if ($(this).val() == "0")
			$('.reporttext').slideDown();
		else
			$('.reporttext').slideUp();
	});
};

$(function(){
	$('.reportbutton').fancybox(reportSettings);
});

