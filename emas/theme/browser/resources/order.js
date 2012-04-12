$(function($) {
    $("#selectpackage input[type='radio']").change(function() {
        var totalcost = 0;
        var practice_subjects = $('input[name="practice_subjects"]:checked').val();
        var include_textbook = $('input[name="include_textbook"]:checked').val() == 'yes';
        var include_expert_answers = $('input[name="include_expert_answers"]:checked').val() == 'yes';
        if ((practice_subjects == 'Maths')||(practice_subjects == 'Science')) {
            totalcost = 150;
            if (include_textbook) {
                totalcost = 200;
            }
        }
        else if (practice_subjects == 'Maths,Science') {
            totalcost = 250;
            if (include_textbook) {
                totalcost = 350;
            }
        }
        if (include_expert_answers) {
            totalcost += 25;
        }
        $('#totalcost').html(totalcost.toFixed(2));
    });
});
