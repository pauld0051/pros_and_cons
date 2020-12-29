// Site wide JS
$(document).ready(function() {
    $(".sidenav").sidenav({ edge: "right" });
    $(".dropdown-trigger").dropdown({ hover: false, 'coverTrigger': false, 'closeOnClick': true });
    $('.tooltipped').tooltip();
    $('.collapsible').collapsible();
    $('.modal').modal();
    $('select').formSelect();
    $('.datepicker').datepicker();
});