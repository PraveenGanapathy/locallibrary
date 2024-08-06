$(document).ready(function(){
    $('#sidebar-nav').on('show.bs.collapse', function () {
      $('a[href="#sidebar-nav"]').html('&#10006;');
    });
  
    $('#sidebar-nav').on('hide.bs.collapse', function () {
      $('a[href="#sidebar-nav"]').html('&#9776;');
    });
  });