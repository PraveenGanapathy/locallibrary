$(document).ready(function(){
    $('.navbar-toggler').on('click', function () {
        var icon = $('#navbar-icon');
        icon.toggleClass('bi-list bi-x');
        if (icon.hasClass('bi-x')) {
            icon.removeClass('bi-list');
        } else {
            icon.removeClass('bi-x');
        }
    });
});