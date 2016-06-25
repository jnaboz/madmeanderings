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

    $(".checkbox").change(function(){
        // Hide or show the delete button
        var $all = $(".checkbox");
        checkbox_set_buttons($all);
    });
});




/* ------------------------------------------------------------------------ */
/* External Functions                                                       */
/* ------------------------------------------------------------------------ */
function checkbox_set_buttons($all){
    var count = 0;
    $all.each(function(){
        if($(this).is(":checked")){
            count = count + 1;
        }
    });
    if(count > 0){
        $("#delete").css("display", "inline-block");
    } else {
        $("#delete").css("display", "none");
    }

    if(count == 1){
        $("#modify").css("display", "inline-block");
    } else {
        $("#modify").css("display", "none");
    }
}
