var player;
var cancelclick = false;
var fadingblack = false;

function playerReady(obj) {
	player = document.getElementById(obj['id']);
	if (!player) alert('Error loading video player.');
};

function addSnapShot(file) {
	if ($('#framerwrapper').css('height') == '0px') openFramer();
	$('#sortable').append('<li class="sortimg" ondblclick="frameDblClick(this);"><div class="delicon" onclick="delFrame(this,event);" title="Delete Frame"></div><div class="editicon" onclick="editFrame(this, event);" title="Edit Frame"></div><div class="uploadicon" onclick="frameDblClick(this.parentNode);" title="Upload Frame"></div><img src="'+file+'" /></li>');
	//$('#sortable').sortable('refresh');
	$( "#sortable" ).sortable({
		revert: true, containment: '#framerwrapper',
		start: function(){cancelclick=true;},
		stop: function(e){cancelclick=false; e.stopPropagation();} 	
	});
	$("#framerwrapper ul, #framerwrapper li" ).disableSelection();
	//$('#sortable .sortdelay').unbind('click').click(frameClick);
	//$('#sortable .sortimg').unbind('dblclick').dblclick(frameDblClick);
};

function delFrame(src, event){
	event.stopPropagation();
	if ($(src).parent().parent().parent().attr('id') != 'framerpanel1')
		$(src).parent().remove();
};

function editFrame(src, event){
	//event.stopPropagation();
	//TODO: add domain check in flash for chance of externally loaded imgs
	s = $(src).parent().find('img').attr('src');
	if (s.indexOf('?') > -1) s = s.substr(0,s.indexOf('?'));
	player.editImg(s);
};

function gifCompile(){
	if (fadingblack) return false;
	fadingblack=true;
	var s = "";
	var waitmin = 0.1;
	var waitmax = 10.0;
	var waitdefault = 0.3;
	var bExit = false;
	$('#sortable input').each(function(index) {
		if (!IsNumeric($(this).val())) {alert('"'+$(this).val()+'" is not a number.'); bExit = true;}
		if ($(this).val() > waitmax) {alert("Maximum wait time exceeded.\nMax wait time: "+waitmax+' seconds.'); bExit = true;}
		if ($(this).val() < waitmin) {alert("Minimum wait time exceeded.\nMin wait time: "+waitmin+' seconds.'); bExit = true;}
	});
	if (bExit) {
		fadingblack = false;
		return false;
	}
	$('#sortable li').each(function(index) {
		s = s + (($(this).hasClass('sortimg')) ? $(this).find('img').attr('src') : $(this).find('input').val()) + "\n";
	});
	$.post('../files/compiler.php', {s: encodeURIComponent(s)},
		function(data){
			$('#framershadow').fadeIn('slow', function(){
				$('#framerpreview div').html(data);
				$('#framerpreview').fadeIn('slow',function(){fadingblack=false;});
				//$('#framerpreview').css('margin-left','-'+($('#framerpreview img').width()/2)+'px');
			});
		}
	);
};

function closePreview(){
	if (fadingblack) return false;
	fadingblack = true;
	$('#framerpreview').fadeOut('slow', function(){
		$('#framershadow').fadeOut('slow', function(){fadingblack=false;});
	});
};

function framer_onload(){
	$( "#draggable" ).draggable({
		connectToSortable: "#sortable",
		helper: "clone",
		revert: "invalid",
		containment: '#framerwrapper'//, axis:'x'
	});
};

function insertFrame(data){
	//alert("Current Frame: "+data);
	$('#comments')[0].contentWindow.gotoDOM('.footerdiv');
	$('#comments')[0].contentWindow.addtag('[v]'+data+'[/v]');
	return "Appended bbcode [v]"+data+"[/v] to your comment.";
};

function openFramer(){
	$('#framerwrapper').animate({height:'120px'},300,'swing');
	$('#mainwrapper').animate({bottom:'120px'},300,'swing');
};

function closeFramer(){
	$('#framerwrapper').animate({height:'0'},300,'swing');
	$('#mainwrapper').animate({bottom:'0'},300,'swing');
};

function frameDblClick(src){
	setUploadImage($(src).find('img').attr('src'));
};

function frameClick(src){
	if (cancelclick) { cancelclick = false; return; }
	s = prompt('Enter a value between 0.01 and 10.0:', $(src).find('input').val());
	if (IsNumeric(s)) $(src).find('input').val(s);
};

function refreshFrames(){
	var date = (new Date()).getTime();
	$('#sortable li img').each(function(index) {
		if (this.src.indexOf('?') > -1) this.src = this.src.substr(0, this.src.indexOf('?'));
		this.src = this.src + '?' + date;
	});
	return "Successfully processed frame edit.";
};

function setUploadImage(url){
	var filename = url.substr(url.indexOf('frameimgs/')+10);
	if (filename.indexOf('?') > -1) filename = filename.substr(0, filename.indexOf('?'));
	$('#comments')[0].contentWindow.gotoDOM('.footerdiv');
	$("#comments").contents().find('#imguploadcell').html('<img src="'+url+'" style="height:100px;" />');
	$("#comments").contents().find('input[name=filename]').val(filename);
	//$("#comments").contents().find('.errdiv').html(filename);	
};