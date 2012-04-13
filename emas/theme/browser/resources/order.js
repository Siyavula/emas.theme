function ordertotal() {
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
}

$(function($) {
    ordertotal();
    $("#selectpackage input[type='radio']").change(ordertotal);
    $("#selectpackage button[type='submit']").click(function () {

        var practice_subjects = $('input[name="practice_subjects"]:checked').val();
        var practice_grade = $('input[name="practice_grade"]:checked').val();
        var include_textbook = $('input[name="include_textbook"]:checked').val() == 'yes';
        var include_expert_answers = $('input[name="include_expert_answers"]:checked').val() == 'yes';
        result = true;
        if (practice_subjects != undefined && practice_grade == undefined) {
            alert('You have to select a grade before you can continue');
            result = false;
        }
        if (practice_subjects == undefined && practice_grade != undefined) {
            alert('You have to specify which subjects you would like to subscribe to before you can continue');
            result = false;
        }
        if (include_textbook && practice_grade == undefined &&
                                practice_subjects == undefined ) {
            alert('You have to specify which subjects and which grade you would like to subscribe to before you can continue');
            result = false;
        }
        if (result == true && parseInt($('#totalcost').html()) == 0) {
            alert('You have to order something before you can continue');
            result = false;
        }

        return result;
    });
});
