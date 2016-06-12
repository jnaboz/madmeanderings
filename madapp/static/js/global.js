/* ------------------------------------------------------------------------ */
/* Document.Ready                                                           */
/* ------------------------------------------------------------------------ */
$(document).ready(function(){
    /* ------------------------------------------------------------------------ */
    /* Initialization                                                           */
    /* ------------------------------------------------------------------------ */
	var NAVTOP = $("#navigation-links").position().top;
	
    /* ------------------------------------------------------------------------ */
    /* Events                                                                   */
    /* ------------------------------------------------------------------------ */
    $(document).scroll(function(){
        var pos = $(document).scrollTop();
		var $nav = $("#navigation-links");
        if(pos > NAVTOP){
			$nav.css("position","fixed");
			$nav.css("top","0");
			$nav.css("left","0");
        } else {
			$nav.css("position", "relative");
        }
    });
});




/* ------------------------------------------------------------------------ */
/* External Functions                                                       */
/* ------------------------------------------------------------------------ */