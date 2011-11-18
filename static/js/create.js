
function resetForm(){
	$('input[type=text]').val('');
	$('textarea').val('');
	$('#url').val('http://');
	$("#name").css({ color:"black", backgroundColor:"" });	
	Recaptcha.reload();
	refreshFileList();
	$('.tagHandler').remove();
	$('#tagsfield').prepend('<ul id="taglist"></ul>');
	loadTagHandler();
}

function IsDefined(val){
	return ((val !== '') && (val !== 'undefined') && (typeof(val) !== 'undefined'));
}

function checkValues(valData) {
	var arrErrors = [];
	
	if (!IsDefined(valData.title)) arrErrors.push("- 'Title' must be defined.");
	if (!IsDefined(valData.description)) arrErrors.push("- 'Description' must be defined.");
    if (!IsDefined(valData.tags)) arrErrors.push("- You must supply some tags.");
	if (!IsDefined(valData.type)) arrErrors.push("- Must select a template.");
	switch (valData.type) {
		case 0: 
			if (!IsDefined(valData.imgtemplate)) arrErrors.push("- Must select an image template layout.");
			if (!IsDefined(valData.imageselect)) arrErrors.push("- Must upload an image.");
			break;
		case 1: if (!IsDefined(valData.videoselect)) arrErrors.push("- Must upload a video."); break;
        case 2: if (!IsDefined(valData.flashselect)) arrErrors.push("- Must upload a flash (.swf) file."); break;
		case 3: if (!IsDefined(valData.url)) arrErrors.push("- Must define a URL."); break;
//		case 4:
//			if ((!IsDefined(valData.htmlselect)) && (!IsDefined(valData.html))) arrErrors.push("- Must upload an HTML file, or input custom HTML.");
//			break;
	}
	if ((!IsDefined(valData.recaptcha_response_field)) && (valData.preview == '0')) arrErrors.push("- 'Captcha' must be completed.");
	
	var errString = arrErrors.join('\n');
	if (errString != '') {
		alert(errString);
		return false;
	} else
		return true;
}

function makePOSTData(postdata, paramlist){
	for (var x in paramlist)
		//postdata[paramlist[x]] = encodeURIComponent($("#"+paramlist[x]).val()).replace("'","%27");
        postdata[paramlist[x]] = $("#"+paramlist[x]).val();
}

function createPage(NotPreview){
	var content = {};
	makePOSTData(content, ["userid","duration","title","description","recaptcha_challenge_field","recaptcha_response_field","url","imageselect","audioselect","videoselect","flashselect"]);
    var tagNames = new Array();
    $("#taglist li.tagItem").each(function () {
        tagNames.push($(this).html());
    });
    content.tags = tagNames.join(',');
	content.preview = NotPreview ? '0' : '1';
	content.type = $("input[name='type']:checked").val();
	content.imgtemplate = $("input[name='imgtemplate']:checked").val();
	content.proportional = ($("input[name='proportion']:checked").length == 1) ? 'yes' : 'no';
	switch(content.type){
		case "image": content.type = 0; break;
		case "video": content.type = 1; break;
        case "flash": content.type = 2; break;
		case "url": content.type = 3; break;
	}
	if (!checkValues(content)) return false;
	//TODO: Fix preview winodow opener...?
	if (!NotPreview) {
        $('body').append('<form id="tmpform" action="/preview" method="post" target="previewWin"></form>');
        for(var i in content) {
            $('#tmpform').append('<input name="'+i+'" value="'+content[i]+'" type="hidden" />');
        }
        window.open('', 'previewWin', '');
        $('#submitbuttons > input:disabled').removeAttr("disabled");
        $('#tmpform').submit().remove();
        //var wnd = window.open('loading', 'previewWin', '');
    } else{
        $.blockUI();
        $.post("/create", content,
            function(data){
                $.unblockUI();
                if (data.success) {
                    resetForm();
                    refreshFileList();
                    AddAjaxDiv('#upload-controller', "ajax_msg_success", 'Adex successfully created: <input type="text" value="'+data.value+'" onclick="this.select();" />');
                } else {
                    AddAjaxDiv('#upload-controller', "ajax_msg_error", data.value);
                }
                //if (data.indexOf('<div id="createerrors">') > -1) wnd.close();
        }, "json");
    }
	return true;
}

function insert(filename){
	var text;
	var farray = filename.split(".");
	var filetype = farray[(farray.length-1)].toLowerCase();
	text = filetype;
	switch (filetype){
		case "mp3":
			text = '<embed src="' + filename + '" autostart=true hidden=true />';
			break;
		case "swf":
			text = '<embed src="' + filename + '" height="100%" width="100%" wmode="transparent" />';
			break;
		case "jpg":
		case "gif":
			text = '<img border="0" src="' + filename + '" />';
			break;
	}

	var textarea = document.getElementById("html");
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

var currTemplateLabel = null;
var currTypeValue = '';
var isTypeChanging = false;

function selectTemplate(obj) {
	var label = $(obj).parent().find("label")[0];
	var openFunc = function(){
				$("#"+obj.value+"options").slideDown(500);
				currTemplateLabel = label;
				currTypeValue = obj.value;
				isTypeChanging = false;
			};
	if ((currTemplateLabel == label) || (isTypeChanging)) return false;
	isTypeChanging = true;
	label.className = "selected";
	if (currTypeValue != '') {
		$(currTemplateLabel).removeClass();
		$("#"+currTypeValue+"options").slideUp(500, openFunc );
	} else
		openFunc();
}

function checkName(data){
	$("#namecheck").html(data);
	$('#name').css("color", "white");
	if (data == '') $("#name").css({ color:"black", backgroundColor:"" });	
	if ((data.indexOf("Invalid") > -1) || (data.indexOf("not a") > -1)) $("#name").css("backgroundColor", "red");
	if (data.indexOf("is a") > -1) $("#name").css("backgroundColor", "green");
}

function refreshFileList(removeid, obj) {
    $('#upload-controller').blockEx();
	var remove_url = (typeof removeid == 'undefined') ? '' : '?d='+removeid;
	//alert(remove_url);
	$('#filedata').load('/ajax/filelist'+remove_url, {},
		function(){
            $('#upload-controller').unblock();
			$('#imageselectspan').html($('#imagelist').remove().html());
			$('#audioselectspan').html($('#audiolist').remove().html());
			$('#videoselectspan').html($('#videolist').remove().html());
			$('#flashselectspan').html($('#flashlist').remove().html());
			$('#htmlselectspan').html($('#htmllist').remove().html());
			$("#uploader").css("display", ($('#maxfileval').remove().html() == '1') ? 'block' : 'none');
			if (obj) $(obj).remove();
			//alert($('#imageselectspan').html());
		});
}

//function startCreateUpload(){
//    for (i in filelist)
//        $('#fileuploader').fileupload('send',{files: filelist[i]});
//}

var filelist = new Array();
function loadCreateUploader(){
    $('#btnAddFile').click(function(e) {
        $('#file').click();
    });

    $('#btnAddFileLib').click(function(e) {
        attachBox.onClosed = addFromLibWindowOnClose;
        $.fancybox(attachBox);
    });

    $('#upload-controller').bind('dragenter', function(){
        $(this).css('outline','2px solid red');
    });
    $('#upload-controller').bind('dragleave drop', function(){
        $(this).css('outline','0');
    });

    $('#fileuploader').fileupload({
        url: '/upload_file',
        dataType: 'json',
        'dropZone': $('#upload-controller'),
        'fileInput': $('#file'),
        sequentialUploads: true,
        maxFileSize: 50000,
        add: function (e, data) {
//                 $.each(data.files, function (index, file) {
//                    var duplicate = false;
//                    for (i in filelist)
//                        if (filelist[i].name == file.name)
//                            duplicate = true;
//                    if (!duplicate){
//                        filelist.push(file);
//                        $('#filelist').append('<li>'+file.name+'</li>');
//                    }
//                });
                $('#upload-controller').blockEx();
                data.submit();
            },
        'progress': function(e, data){
                var progress = parseInt(data.loaded / data.total * 100, 10);
                //drawImageFit(canvas, img, progress);
                //$('#results').append('<p>'+progress+'-'+data.files[0].name+'</p>');
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
                if (data.result.success) {
                    refreshFileList();
                } else {
                    $('#upload-controller').unblock();
                    AddAjaxDiv('#upload-controller', "ajax_msg_error", data.result.error);
                }
            }
    });
}

function loadTagHandler(){
	$('#taglist').tagHandler({
	    getURL: '/ajax/taglist',
	    autocomplete: true
	});
}

function create_onload() {
	refreshFileList();
	loadTagHandler();

	$(".tooltip").focus( function(){ $('#'+$(this).attr('id')+'hint').css('display','inline'); } );
	$(".tooltip").blur( function(){ $('#'+$(this).attr('id')+'hint').css('display','none'); } );

	$(".typeradio label").click(function(){ selectTemplate($("#"+$(this).attr('for'))[0]); });

	if (!isbanned) {
		loadCreateUploader();
		Recaptcha.create("6LdKer0SAAAAAEj2Tu5XjFY2VajoSy8eltRpjfaN", "recaptchadivframe", 
				   {	theme: "clean",
				     	callback: Recaptcha.focus_response_field 
				   });
	}
}