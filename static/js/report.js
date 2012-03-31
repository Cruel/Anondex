var reportSettings = {
    'closeBtn'      :   false,
    'scrolling'     :   'no',
	'padding'		:	20,
	'overlayColor'	:	'black',
	'modal'			:	true,
	'overlayOpacity':	0.6,
	'afterShow'     :	reportWindowOnLoad
};

function reportSubmit() {
	$.post(reportSettings['href'], {'type':$('.reportselect').val(), 'comment':$('.reporttext').val()},
			function(data){
                reportSettings['type'] = 'html';
				$.fancybox(data,reportSettings);
			});
}

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
        $.fancybox.update()
	});
}

$(function(){
    $('.reportbutton').click(function(){
        reportSettings['type'] = 'ajax';
        reportSettings['href'] = $(this).data('report-url');
        $.fancybox(reportSettings);
    });
});

