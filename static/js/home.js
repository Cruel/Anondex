
var fadeScaleLock = false;
function fadeScale2(objSelector, fadeIn, callback){
    if (fadeIn)
        $(objSelector+' > *').fadeTo(0,0);
    else
        $(objSelector+' .document-script').remove(); // Correct layout transition problem due to script <div>
	$(objSelector).css('visibility','visible');
    var lastIndex = $(objSelector+' > *').length - 1;
    if (lastIndex >= 0) {
        fadeScaleLock = true;
        $(objSelector+' > *').each(function(index) {
            $(this).delay(index*70).fadeTo(400,(fadeIn?1:0));
            if (index == lastIndex)
                setTimeout(function(){
                    if (callback) callback();
                    fadeScaleLock = false;
                },index*70+350);
        });
    }
}

function fadeScale(objSelector, fadeIn, callback){
    if (!fadeIn)
        $(objSelector+' .document-script').remove(); // Correct layout transition problem due to script <div>
	$(objSelector).css('visibility','visible');
    if (callback) callback();

}

function browse_onload(){
    $('.browsetable > div').click(function(){
        window.location = $(this).attr('rel');
    });
}

// https://gist.github.com/854622
function home_onload(){
	var
		History = window.History,
		$ = window.jQuery,
		document = window.document;

    //fadeScale('#creatediv', true);
    $('#sidebar').load('/ajax/sidebar',function(){
        fadeScale('#sidebar', true);
        $('#sidebar').ajaxify();
        comment_cluetips();
    });

	// Check to see if History.js is enabled for our Browser
	if ( !History.enabled ) {
		return false;
	}

	// Wait for Document
	$(function(){
		// Prepare Variables
		var
			/* Application Specific Variables */
			contentSelector = '#content',
			$content = $(contentSelector).filter(':first'),
			contentNode = $content.get(0),
			$menu = $('#menu,#nav,nav:first,.nav:first').filter(':first'),
			activeClass = 'active',
			activeSelector = '.active',
			menuChildrenSelector = '> li,> ul > li',
			/* Application Generic Variables */
			$body = $(document.body),
			rootUrl = History.getRootUrl(),
			scrollOptions = {
				duration: 500,
				easing:'swing'
			};
		
		// Ensure Content
		if ( $content.length === 0 ) {
			$content = $body;
		}
		
		// Internal Helper
		$.expr[':'].internal = function(obj, index, meta, stack){
			// Prepare
			var
				$this = $(obj),
				url = $this.attr('href')||'',
				isInternalLink;
			
			// Check link
			isInternalLink = url.substring(0,rootUrl.length) === rootUrl || url.indexOf(':') === -1;
			
			// Ignore or Keep
			return isInternalLink;
		};
		
		// HTML Helper
		var documentHtml = function(html){
			// Prepare
			var result = String(html)
				.replace(/<\!DOCTYPE[^>]*>/i, '')
				.replace(/<(html|head|body|title|meta|script)([\s\>])/gi,'<div class="document-$1"$2')
				.replace(/<\/(html|head|body|title|meta|script)\>/gi,'</div>')
			;
			
			// Return
			return result;
		};

        // Active Menu highlightwe
        var highlightActive = function(url){
            if (!url) url = History.getState().url.replace(rootUrl,'');
            $menuChildren = $menu.find(menuChildrenSelector);
            $menuChildren.filter(activeSelector).removeClass(activeClass);
            $menuChildren = $menuChildren.has('a[href^="'+url+'"],a[href^="/'+url+'"],a[href^="'+url+'"]');
            if ( $menuChildren.length === 1 ) { $menuChildren.addClass(activeClass); }
        }
        highlightActive();
		
		// Ajaxify Helper
		$.fn.ajaxify = function(){
			// Prepare
			var $this = $(this);
			
			// Ajaxify
			$this.find('a:internal:not(.no-ajaxy)').click(function(event){
                if (fadeScaleLock){
                    event.preventDefault();
				    return false;
                }
				// Prepare
				var
					$this = $(this),
					url = $this.attr('href'),
					title = $this.attr('title')||null;
				
				// Continue as normal for cmd clicks etc
				if ( event.which == 2 || event.metaKey ) { return true; }
				
				// Ajaxify this link
				History.pushState(null,title,url);
				event.preventDefault();
				return false;
			});
			
			// Chain
			return $this;
		};
		
		// Ajaxify our Internal Links
		$body.ajaxify();
		
		// Hook into State Changes
		$(window).bind('statechange',function(){
            //if (fadeScaleLock) return false;
			// Prepare Variables
			var
				State = History.getState(),
				url = State.url,
				relativeUrl = url.replace(rootUrl,'');

			// Set Loading
			$body.addClass('loading');

            // Update the menu
            highlightActive(relativeUrl);

			// Start Fade Out
			// Animating to opacity to 0 still keeps the element's height intact
			// Which prevents that annoying pop bang issue when loading in new content
			//$content.animate({opacity:0},800);
            //$(contentSelector+' > div').fadeOut(300, function(){
            fadeScale(contentSelector+' > div', false, function(){

                // Ajax Request the Traditional Page
                $.ajax({
                    url: url,
                    success: function(data, textStatus, jqXHR){
                        // Prepare
                        var
                            $data = $(documentHtml(data)),
                            $dataBody = $data.find('.document-body:first'),
                            $dataContent = $dataBody.find(contentSelector).filter(':first'),
                            $menuChildren, contentHtml, $scripts;
                        //alert($data.html());
                        // Fetch the scripts
                        $scripts = $dataContent.find('.document-script');
                        if ( $scripts.length ) {
                            $scripts.detach();
                        }

                        // Fetch the content
                        contentHtml = $dataContent.html()||$data.html();
                        if ( !contentHtml ) {
                            document.location.href = url;
                            return false;
                        }



                        // Update the content
                        $content.stop(true,true);
                        $content.html(contentHtml).ajaxify();//.css('opacity',100).show(); /* you could fade in here if you'd like */
                        fadeScale(contentSelector+' > div', true);

                        // Update the title
                        document.title = $data.find('.document-title:first').text();
                        try {
                            document.getElementsByTagName('title')[0].innerHTML = document.title.replace('<','&lt;').replace('>','&gt;').replace(' & ',' &amp; ');
                        }
                        catch ( Exception ) { }

                        // Add the scripts
                        $scripts.each(function(){
                            var $script = $(this), scriptText = $script.html(), scriptNode = document.createElement('script');
                            scriptNode.appendChild(document.createTextNode(scriptText));
                            contentNode.appendChild(scriptNode);
                        });

                        // Complete the change
                        if ( $body.ScrollTo||false ) { $body.ScrollTo(scrollOptions); } /* http://balupton.com/projects/jquery-scrollto */
                        $body.removeClass('loading');

                        // Inform Google Analytics of the change
                        if ( typeof window.pageTracker !== 'undefined' ) {
                            window.pageTracker._trackPageview(relativeUrl);
                        }

                        // Inform ReInvigorate of a state change
                        if ( typeof window.reinvigorate !== 'undefined' && typeof window.reinvigorate.ajax_track !== 'undefined' ) {
                            reinvigorate.ajax_track(url);
                            // ^ we use the full url here as that is what reinvigorate supports
                        }
                    },
                    error: function(jqXHR, textStatus, errorThrown){
                        document.location.href = url;
                        return false;
                    }
                }); // end ajax
            });

		}); // end onStateChange

	}); // end onDomLoad

}//);(window); // end closure