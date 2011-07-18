
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
};

function testy(){
	$(".progressbar").progressbar({value: 70});
};

function IsDefined(val){
	return ((val !== '') && (val !== 'undefined') && (typeof(val) !== 'undefined'));
};

function checkValues(valData) {
	var arrErrors = [];
	
	if (!IsDefined(valData.title)) arrErrors.push("- 'Title' must be defined.");
	if (!IsDefined(valData.description)) arrErrors.push("- 'Description' must be defined.");
	if (!IsDefined(valData.type)) arrErrors.push("- Must select a template.");
	switch (valData.type) {
		case 0: 
			if (!IsDefined(valData.imgtemplate)) arrErrors.push("- Must select an image template layout.");
			if (!IsDefined(valData.imageselect)) arrErrors.push("- Must upload an image.");
			break;
		case 1: if (!IsDefined(valData.videoselect)) arrErrors.push("- Must upload a video."); break;
		case 2: if (!IsDefined(valData.url)) arrErrors.push("- Must define a URL."); break;
		case 3:
			if ((!IsDefined(valData.htmlselect)) && (!IsDefined(valData.html))) arrErrors.push("- Must upload an HTML file, or input custom HTML.");
			break;
		case 4: if (!IsDefined(valData.flashselect)) arrErrors.push("- Must upload a flash (.swf) file."); break;
	}
	if ((!IsDefined(valData.recaptcha_response_field)) && (valData.preview == '0')) arrErrors.push("- 'Captcha' must be completed.");
	
	var errString = arrErrors.join('\n');
	if (errString != '') {
		alert(errString);
		return false;
	} else
		return true;
};

function makePOSTData(postdata, paramlist){
	for (var x in paramlist)
		//eval("postdata."+paramlist[x]+"= '"+ encodeURIComponent($("#"+paramlist[x]).val()).replace("'","%27") +"'");
		postdata[paramlist[x]] = encodeURIComponent($("#"+paramlist[x]).val()).replace("'","%27");
};

function createPage(NotPreview){
	$('#results').html('');
	var content = {};
	makePOSTData(content, ["duration","title","name","description","recaptcha_challenge_field","recaptcha_response_field","url","imageselect","musicselect","videoselect","flashselect","html","htmlselect"]);
    var tagNames = new Array();
    $("#taglist li.tagItem").each(function () {
        tagNames.push($(this).html());
    });
    content.tags = tagNames.join(',');
	content.preview = NotPreview ? '0' : '1';
	if (content.url == 'http%3A%2F%2F') content.url = '';
	content.type = $("input[name='type']:checked").val();
	content.imgtemplate = $("input[name='imgtemplate']:checked").val();
	content.proportional = ($("input[name='proportion']:checked").length == 1) ? 'yes' : 'no';
	switch(content.type){
		case "image": content.type = 0; break;
		case "video": content.type = 1; break;
		case "url": content.type = 2; break;
		case "html": content.type = 3; break;
		case "flash": content.type = 4; break;
	}
	if (!checkValues(content)) return false;
	$('#results').html('<img border="0" src="images/working.gif" /> Loading... please wait...');
	//TODO: Fix preview winodow opener...?
	if (!NotPreview) var wnd = window.open('loading', 'previewWin', '');
	
	$.post("../func/create.php", content,
		function(data){
			$('#results').html(data);
			if (!NotPreview) {
				if (data == 'Preview Generated!') {
					window.open('preview', 'previewWin');
					$('#submitbuttons > input:disabled').removeAttr("disabled");
				} else
					wnd.close();
			} else if (data.indexOf('<div id="createsuccess">') > -1) {
				$('#content').load('includes/create.php',
						function(){
							//create_onload();
							resetForm();
							$('#results').html(data);
						});
			}
			if (data.indexOf('<div id="createerrors">') > -1) wnd.close(); 
		});
	return true;
};

function insert(filename)
{
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
};

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
};

function checkName(data){
	$("#namecheck").html(data);
	$('#name').css("color", "white");
	if (data == '') $("#name").css({ color:"black", backgroundColor:"" });	
	if ((data.indexOf("Invalid") > -1) || (data.indexOf("not a") > -1)) $("#name").css("backgroundColor", "red");
	if (data.indexOf("is a") > -1) $("#name").css("backgroundColor", "green");
};

function refreshFileList(removeid, uploadid) {
	removeid = (typeof removeid == 'undefined') ? '' : '&d='+removeid;
	//alert(removeid);
	$('#filelist').load('/ajax/filelist'+removeid, {},
		function(){
			$('#imageselectspan').html($('#imagelist').remove().html());
			$('#musicselectspan').html($('#musiclist').remove().html());
			$('#videoselectspan').html($('#videolist').remove().html());
			$('#flashselectspan').html($('#flashlist').remove().html());
			$('#htmlselectspan').html($('#htmllist').remove().html());
			$("#uploader").css("display", ($('#maxfileval').remove().html() == '1') ? 'block' : 'none');
			if (typeof uploadid != 'undefined') $('#log div#'+uploadid).remove();
			//alert($('#imageselectspan').html());
		});
};

function loadCreateUploader(){
	$(function(){
		$('#upload-controller').swfupload({
			upload_url: "func/upload-file.php?i="+document.cookie.match(/PHPSESSID=[^;]+/),
			file_post_name: 'uploadfile',
			file_size_limit : "10024",
			file_types : "*.jpg;*.png;*.gif;*.mp3;*.mid;*.flv;*.mp4;*.swf;*.html;*.htm",
			file_types_description : "Allowed Files",
			file_upload_limit : 15,
			flash_url : "js/swfupload/swfupload.swf",
			button_image_url : 'js/swfupload/wdp_buttons_upload_114x29.png',
			button_width : 114,
			button_height : 29,
			button_placeholder : $('#swfupload_placeholder')[0],
			debug: false
		})
			.bind('fileQueued', function(event, file){
				var listitem='<div id="'+file.id+'" >'+
					'<span class="progressbar" ></span><table class="fileinfo"><tr>'+
					'<td class="filenamecell"><b>'+file.name+'</b></td>'+
					'<td class="statuscell" >Queued</td>'+
					'<td class="progressvalue">0% (0/'+Math.round(file.size/1024)+' KB)</td>'+
					'<td class="cancelcell"><input type="button" value="Cancel" /></td>'+
					'</tr></table></div>';
				$('#log').append(listitem);
				$('div#'+file.id+' input').bind('click', function(){
					var swfu = $.swfupload.getInstance('#upload-controller');
					swfu.cancelUpload(file.id);
					$('div#'+file.id).slideUp('fast');
				});
				// start the upload since it's queued
				$(this).swfupload('startUpload');
			})
			.bind('fileQueueError', function(event, file, errorCode, message){
				alert('Size of the file '+file.name+' is greater than limit');
			})
			.bind('fileDialogComplete', function(event, numFilesSelected, numFilesQueued){
				$('#queuestatus').text('Files Selected: '+numFilesSelected+' / Queued Files: '+numFilesQueued);
			})
			.bind('uploadStart', function(event, file){
				$('#log div#'+file.id).find('.statuscell').text('Uploading...');
				$('#log div#'+file.id).find('.progressvalue').text('0%');
				//$('#log div#'+file.id).find('.cancelcell input').hide();
				//disable cancel button?
			})
			.bind('uploadProgress', function(event, file, bytesLoaded){
				//Show Progress
				var percentage=Math.round((bytesLoaded/file.size)*100);
				//$('#log div#'+file.id).find('span.progressbar').css('width', percentage+'%');
				$('#log div#'+file.id+" .progressbar").progressbar({value: percentage});
				$('#log div#'+file.id).find('.progressvalue').text(percentage+'% ('+Math.round(bytesLoaded/1024)+'/'+Math.round(file.size/1024)+' KB)');
				//alert(percentage);
			})
			.bind('uploadSuccess', function(event, file, serverData){
				if (serverData != '') alert(serverData);
				//$('#log div#'+file.id).find('span.progressbar').css('width', '100%');
				refreshFileList('',file.id);
				//$('#log div#'+file.id).remove();
			})
			.bind('uploadComplete', function(event, file){
				// upload has completed, try the next one in the queue
				$(this).swfupload('startUpload');
			});
		
	});	
};

function loadTagHandler(){
	$('#taglist').tagHandler({
	    //getData: { a: 'taglist', i: '' },
	    getURL: '/ajax/taglist',
	    autocomplete: true
	});
};

function create_onload() {
	refreshFileList();
	loadTagHandler();
	//$(".tooltip").focus( function(){ this.parentNode.getElementsByTagName("span")[0].style.display = "inline"; } );
	//$(".tooltip").blur( function(){ this.parentNode.getElementsByTagName("span")[0].style.display = "none"; } );
	$(".tooltip").focus( function(){ $('#'+$(this).attr('id')+'hint').css('display','inline'); } );
	$(".tooltip").blur( function(){ $('#'+$(this).attr('id')+'hint').css('display','none'); } );
	//$(".typeradio input").click(function(){ selectTemplate(this); });
	//$(".typeradio label").click(function(){ selectTemplate($(this).parent("input")); }); // IE correction
	//$(".typeradio label").click(function(){ selectTemplate(this.parentNode.getElementsByTagName("input")[0]); }); // IE correction
	$(".typeradio label").click(function(){ selectTemplate($("#"+$(this).attr('for'))[0]); });
	//$("label[for='"+currTypeValue+"radio']").click();
	if (!isbanned) {
		//loadCreateUploader();
		Recaptcha.create("6LdKer0SAAAAAEj2Tu5XjFY2VajoSy8eltRpjfaN", "recaptchadivframe", 
				   {	theme: "clean",
				     	callback: Recaptcha.focus_response_field 
				   });
	}
};