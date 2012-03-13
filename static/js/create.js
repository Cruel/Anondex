
function resetForm(){
	$('input[type=text]').val('');
	$('textarea').val('');
	$('#url').val('http://');
	$("#name").css({ color:"black", backgroundColor:"" });	
	Recaptcha.reload();
	refreshFileList();

//    loadTagHandler('#taglist','create');
    $('#createbutton').attr("disabled", "disabled");
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
    if (valData.preview == '0'){
        if (!IsDefined(valData.recaptcha_response_field))
            arrErrors.push("- 'Captcha' must be completed.");
        if (valData.tos == 'no')
            arrErrors.push("- 'You must agree to the Terms of Service to create content.");
    }
	
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
//    var tagNames = new Array();
//    $("#taglist li.tagItem").each(function () {
//        tagNames.push($(this).html());
//    });
    content.tags = $('#taglist').tagHandler('getSerializedTags');//tagNames.join(',');
	content.preview = NotPreview ? '0' : '1';
	content.type = $("input[name='type']:checked").val();
	content.imgtemplate = $("input[name='imgtemplate']:checked").val();
	content.proportional = ($("input[name='proportion']").is(':checked')) ? 'yes' : 'no';
    content.tos = ($("#tos").is(':checked')) ? 'yes' : 'no';
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
        $('#createbutton').removeAttr("disabled");
        $('#tmpform').submit().remove();
        //var wnd = window.open('loading', 'previewWin', '');
    } else{
        $.blockUI();
        $.post("/create/post", content,
            function(data){
                $.unblockUI();
                if (data.success) {
                    resetForm();
                    AddAjaxDiv('#submitbuttons', "ajax_msg_success", 'Adex successfully created: <input type="text" value="'+data.value+'" onclick="this.select();" />');
                } else {
                    AddAjaxDiv('#submitbuttons', "ajax_msg_error", data.value);
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

function refreshFileList(action, id) {
    $('#media-controller').blockEx();
    var mod_url = '';
    if (action) {
        mod_url = '?action='+action;
        mod_url += (typeof id == 'undefined') ? '' : '&id='+id;
    }
	$('#filedata').load('/ajax/filelist'+mod_url, {},
		function(){
            $('#media-controller').unblock();
            loadTagHandler('taglist','create');
			$('#imageselectspan').html($('#imagelist').remove().html());
			$('#audioselectspan').html($('#audiolist').remove().html());
			$('#videoselectspan').html($('#videolist').remove().html());
			$('#flashselectspan').html($('#flashlist').remove().html());
			$('#htmlselectspan').html($('#htmllist').remove().html());
//			if (obj) $(obj).remove();
			//alert($('#imageselectspan').html());
            bindThumbEvents('#filedata');
		});
}

function loadCreateUploader(){
    $('#btnAddFile').click(function(e) {
        //$('#file').click();
        $.fancybox(uploadBox);
    });

    $('#btnAddFileLib').click(function(e) {
        attachBox.afterClose = addFromLibWindowOnClose;
        $.fancybox(attachBox);
    });
}

function loadTagHandler(id, querystring){
    $('#'+id).parent().replaceWith('<ul id="'+id+'"></ul>');
    //$(selector+' #tagsfield').prepend('<ul class="taglist"></ul>');
    $('#'+id).tagHandler({
        getURL: '/ajax/taglist?'+querystring,
        autocomplete: true
    });
}

function create_onload() {
	refreshFileList();

	$(".tooltip").focus( function(){ $('#'+$(this).attr('id')+'hint').css('display','inline'); } );
	$(".tooltip").blur( function(){ $('#'+$(this).attr('id')+'hint').css('display','none'); } );

	$(".typeradio label").click(function(){ selectTemplate($("#"+$(this).attr('for'))[0]); });

	if (!isbanned) {
		loadCreateUploader();
		Recaptcha.create("6LdkaM0SAAAAAHoGAvLwosknMLA5pL-J7DYKSVj0", "recaptchadivframe",
				   {	theme: "clean",
				     	callback: Recaptcha.focus_response_field 
				   });
	}
}