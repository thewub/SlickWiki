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

});