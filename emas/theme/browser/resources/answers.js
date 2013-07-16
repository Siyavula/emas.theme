$(function() {

   $("a.show-answers").click(function() {
        $(this).parents('.answer-section').children('.answer-content').toggle();
        $(this).toggle();
    });

}); 
