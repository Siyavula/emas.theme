$(function() {

   $(".slide0 .how-works").live("click", function() {
        $('.slide0').addClass('hidden');
        $('.slide1').removeClass('hidden');
    });
   $(".slide1 .next-button").live("click", function() {
        var answer = $('#demo_answer').attr('value')
        if ( answer == "" ) {
            // show tooltips
            $('#tooltip1').removeClass('hidden');
            $('#tooltip2').removeClass('hidden');
        }
        else {
            $('.slide1').addClass('hidden');
            $('.slide2').removeClass('hidden');
            if ( answer == "2" ) {
                // hide incorrect
                $('#answer-incorrect-img').addClass('hidden');
                $('#answer-correct-img').removeClass('hidden');
            }
            else {
                // else hide correct
                $('#answer-correct-img').addClass('hidden');
                $('#answer-incorrect-img').removeClass('hidden');
            }
            // hide tooltips (in case they are shown)
            $('#tooltip1').addClass('hidden');
            $('#tooltip2').addClass('hidden');
        }
    });
   $(".slide2 .next-button").live("click", function() {
        $('.slide2').addClass('hidden');
        $('.slide3').removeClass('hidden');
    });
   $(".slide3 .next-button").live("click", function() {
        $('.slide3').addClass('hidden');
        $('.slide4').removeClass('hidden');
    });
   $(".slide4 .next-button").live("click", function() {
        $('.slide4').addClass('hidden');
        $('.slide5').removeClass('hidden');
    });
   $(".slide5 .next-button").live("click", function() {
        $('.slide5').addClass('hidden');
        $('.slide6').removeClass('hidden');
    });
   $(".slide6 .next-button").live("click", function() {
        $('.slide6').addClass('hidden');
        $('.slide0').removeClass('hidden');
    });

   $(".slide1 .prev-button").live("click", function() {
        $('.slide1').addClass('hidden');
        $('.slide0').removeClass('hidden');
        // hide tooltips (in case they are shown)
        $('#tooltip1').addClass('hidden');
        $('#tooltip2').addClass('hidden');
    });
   $(".slide2 .prev-button").live("click", function() {
        $('.slide2').addClass('hidden');
        $('.slide1').removeClass('hidden');
    });
   $(".slide3 .prev-button").live("click", function() {
        $('.slide3').addClass('hidden');
        $('.slide2').removeClass('hidden');
    });
   $(".slide4 .prev-button").live("click", function() {
        $('.slide4').addClass('hidden');
        $('.slide3').removeClass('hidden');
    });
   $(".slide5 .prev-button").live("click", function() {
        $('.slide5').addClass('hidden');
        $('.slide4').removeClass('hidden');
    });
   $(".slide6 .prev-button").live("click", function() {
        $('.slide6').addClass('hidden');
        $('.slide5').removeClass('hidden');
    });

}); 
