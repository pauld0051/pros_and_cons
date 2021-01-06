// Site wide JS
$(document).ready(function() {
    $(".sidenav").sidenav({ edge: "right" });
    $(".dropdown-trigger").dropdown({ hover: false, 'coverTrigger': false, 'closeOnClick': true });
    $('.tooltipped').tooltip();
    $('.collapsible').collapsible();
    $('.modal').modal();
    $('select').formSelect();
    $('.datepicker').datepicker({
        format: "dd mmmm, yyyy",
        yearRange: 99,
        maxDate: new Date(),
        showClearBtn: true,
        selectMonths: true,
        i18n: {
            done: "Select"
    }});
});