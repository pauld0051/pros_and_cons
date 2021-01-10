// Site wide JS
$(document).ready(function() {
    $(".sidenav").sidenav({ edge: "right" });
    $(".dropdown-trigger").dropdown({ hover: false, 'coverTrigger': false, 'closeOnClick': true });
    $('.tooltipped').tooltip();
    $('.collapsible').collapsible();
    $('.modal').modal();
    $('select').formSelect();
    $('.datepicker').datepicker({
        showClearBtn: true,
        selectMonths: true,
        yearRange: 90,
        format: "dd mmmm, yyyy",
        minDate: new Date(1920, 1, 1),
        i18n: {
            done: "Select"
        }           
        });
});