$(document).ready(function() {

    /* Sortable tables */
    var table = $('.table-sortable').stupidtable();
    table.bind('aftertablesort', function (event, data) {
        // Add arrow to indicate that column was sorted
        // data.column - the index of the column sorted after a click
        // data.direction - the sorting direction (either asc or desc)

        var th = $(this).find('th');
        th.find('.arrow').remove();

        if (data.direction === 'asc') {
            th.eq(data.column).append('<i class="arrow fa fa-angle-up"></i>');
        } else {
            th.eq(data.column).append('<i class="arrow fa fa-angle-down"></i>');
        }
        // var arrow = data.direction === "asc" ? "↑" : "↓";
        // th.eq(data.column).append('<span class="arrow">' + arrow +'</span>');
    });
    /* End of sortable tables */

    // When our page loads, check to see if it contains an anchor
    scroll_if_anchor(window.location.hash);

    // Intercept all anchor clicks
    $("body").on("click", "a[href^='#']", scroll_if_anchor);

});


/**
  * From http://stackoverflow.com/a/13067009/3438044
  * Check an href for an anchor. If exists, and in document, scroll to it.
  * If href argument omitted, assumes context (this) is HTML Element,
  * which will be the case when invoked by jQuery after an event
  */
function scroll_if_anchor(href) {

    // Offset in px
    var fromTop = 60;

    href = typeof(href) == "string" ? href : $(this).attr("href");

    // If href missing, ignore
    if(!href) return;

    // If our Href points to a valid, non-empty anchor, and is on the same page (e.g. #foo)
    // Legacy jQuery and IE7 may have issues: http://stackoverflow.com/q/1593174
    var $target = $(href);

    // Older browsers without pushState might flicker here, as they momentarily
    // jump to the wrong position (IE < 10)
    if($target.length) {
        $('html, body').animate({ scrollTop: $target.offset().top - fromTop }, 200);
        if(history && "pushState" in history) {
            history.pushState({}, document.title, window.location.pathname + href);
            // Hack because the :target pseudoselector doesn't work with this code
            $('.target').removeClass('target');
            $target.addClass('target');
            return false;
        }
    }
}
