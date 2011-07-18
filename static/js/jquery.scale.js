
/* Plugin source: http://staff.osuosl.org/~rob/jquery.scale/index.htm */

(function($){                               // anonymous function wrapper

    $.fn.extend({                           // attach new method to jQuery
    
        scale: function( center, stretch ){// declare plugin name and parameter
        
            // iterate over current set of matched elements
            return this.each( function()
            {

                // parse the arguments into flags
            	/*
                var center = false;
                var stretch = false;
                if( arg1 == "center" || arg2 == "center")
                    center = true;
                if( arg1 == "stretch" || arg2 == "stretch")
                    stretch = true;
            	*/
                // capture the object
                var obj = $(this);
                
                // if this is the plugin's first run on the object, and the
                // object is an image, force a reload
                if( obj.attr('src') && 
                    !obj.data('jquery_scale_orig-height') ){
                    

                    var date = new Date();
                    var cursrc = obj.attr("src");
                    var newsrc = cursrc;
                    if( cursrc.indexOf('?') != -1 )
                        newsrc = cursrc.substring( 0, cursrc.indexOf('?'));
                    newsrc = newsrc + "?" + date.getTime();
                    obj.attr( "src", newsrc );

					// For I.E. 6-8 support as it requires a new image for scaling
					if($.support.leadingWhitespace)
						obj.attr("src", cursrc);
                    this.onload = scale;
                    
                } else {
                    scale();
                }
                
                // plugin's main function
                function scale()
                {
                    // if this is the plugin's first run on the object, capture
                    // the object's original dimensions
                    if( !obj.data('jquery_scale_orig-height') ){
                        obj.data('jquery_scale_orig-height', obj.height() );
                        obj.data('jquery_scale_orig-width', obj.width() );
                        
                    
                    // if this is NOT the plugin's first run on the object,
                    // reset the object's dimensions
                    } else {           
                        obj.height( parseInt( 
                            obj.data('jquery_scale_orig-height') ) );
                        obj.width( parseInt( 
                            obj.data('jquery_scale_orig-width') ) );
                        

                    }

                    
                    // Object too tall, but width is fine. Need to shorten.
                    if( obj.outerHeight(  ) > obj.parent().height() && 
                        obj.outerWidth(  ) <= obj.parent().width() ){

                        matchHeight();       
                    }
                    
                    // Object too wide, but height is fine. Need to diet.
                    else if( obj.outerWidth(  ) > obj.parent().width() && 
                             obj.outerHeight(  ) <= obj.parent().height() ){

                        matchWidth();    
                    }
                    
                    // Object too short and skinny. If "stretch" option enabled,
                    // match the dimenstion that is closer to being correct.
                    else if( obj.outerWidth(  ) < obj.parent().width() && 
                             obj.outerHeight(  ) < obj.parent().height() &&
                             stretch ){
                      
                        if( obj.parent().height()/obj.outerHeight(  ) <= 
                            obj.parent().width()/obj.outerWidth(  ) ){
                            
                            matchHeight();
                            
                        } else {
                            matchWidth();
                        }
                    
                    // Object too tall and wide. Need to match the dimension 
                    // that is further from being correct.
                    } else if( obj.outerWidth(  ) > obj.parent().width() && 
                               obj.outerHeight(  ) > obj.parent().height() ){
                               
                        if( obj.parent().height()/obj.outerHeight(  ) >
                            obj.parent().width()/obj.outerWidth(  ) ){
                            
                            matchWidth();
                            
                        } else {
                            matchHeight();
                        }                            

                    }//else, object is the same size as the parent. Do nothing.

                    // if the center option is enabled, also center the object 
                    // within the parent
                    if( center ){
                        obj.css( 'position', 'relative' );
                        obj.css( 'margin-top', 
                        		Math.round(obj.parent().height()/2 - 
                                        obj.outerHeight(  )/2)  );
                        obj.css( 'margin-left', 
                        		Math.round(obj.parent().width()/2 - 
                                        obj.outerWidth(  )/2)  );
                    }

                    // reset the onload pointer so the object doesn't flicker
                    // when reloaded other ways.
                    this.onload = null;                   
                
                };   //END scale
                
                // match the height while maintaining the aspect ratio
                function matchHeight()
                {
                    obj.width(Math.round( obj.outerWidth(  ) * 
                        obj.parent().height()/obj.outerHeight(  ) - 
                        (obj.outerWidth(  ) - obj.width())));
                    obj.height(Math.round( obj.parent().height() - 
                        (obj.outerHeight(  ) - obj.height()) ));
                };
                
                // match the width while maintaining the aspect ratio
                function matchWidth()
                {
                    obj.height(Math.round(  obj.outerHeight(  ) * 
                        obj.parent().width()/obj.outerWidth(  ) - 
                        (obj.outerHeight(  ) - obj.height())  ));
                    obj.width(Math.round( obj.parent().width() - 
                        (obj.outerWidth(  ) - obj.width())));
                };
                            
            });
            
			//if (typeof callback === "function") callback.back(this);
        }
    });
})(jQuery);
