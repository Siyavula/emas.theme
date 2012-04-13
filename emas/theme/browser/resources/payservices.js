jQuery(function($){
    $('a.payservice-overlay').prepOverlay({
        subtype: 'ajax',
        filter: '#content',
        closeselector: '[name=form.button.cancel]',
        config: {onClose : function (e) {
                    var overlay = this.getOverlay();
                    if (jQuery('div.payservice-form', overlay).length == 0) {
                        location.reload();
                    }
                }
        }
    });
});

function buyQuestions(event) {
    event.preventDefault();
    element = jQuery('input#credits-to-buy');
    var amount = parseInt(jq(element).attr('value'));
    if (isNaN(amount)) {
        alert("'" + jq(element).attr('value') + "' is not a valid number!");
        jq(element).attr('value', 0);
        return false;
    }
    jQuery.ajax({
        url: '@@json-buyquestions',
        dataType: 'json',
        data: {'buy': amount},
        success: onQuestionsBought,
        error: errorHandler,
    });
}

function onQuestionsBought(data, textStatus, jqXHR) {
    jQuery('div#status-message').html(data.message);
    jQuery('div.payservice-form').remove()
    jQuery('div#pay-success').show();
}


function startTransaction(event) {
    event.preventDefault();
    element = jQuery('input#credits-to-buy');
    var qty = parseInt(jq(element).attr('value'));
    if (isNaN(qty)) {
        alert("'" + jq(element).attr('value') + "' is not a valid number!");
        jq(element).attr('value', 0);
        return false;
    }
    jQuery.ajax({
        url: '@@json-start-transaction',
        dataType: 'json',
        data: {'quantity': qty},
        success: function(data, textStatus, jqXHR) {
            jQuery('div#status-message').html(data.message);
            jQuery('div.payservice-form').remove();
            jQuery('input[name=p1]').attr('value', data.vcs_terminal_id);
            jQuery('input[name=p2]').attr('value', data.transaction_id);
            jQuery('input[name=p3]').attr('value', data.description);
            jQuery('input[name=p4]').attr('value', data.totalcost);
            jQuery('input[name=m1]').attr('value', data.quantity);
            jQuery('input[name=Hash]').attr('value', data.hash);
            jQuery('div#vcs-purchase-form').show();
        },
        error: errorHandler,
    });
}

function errorHandler(jqXHR, textStatus, errorThrown) {
    alert(textStatus);
    element = jQuery('input#credits-to-buy');
    jQuery(element).attr('value', 0);
}

function registerForMoreExercise(event) {
    return register(event,
                    '@@json-register-for-more-exercise',
                    'registerformoreexercise',
                    'emas.theme.registerformoreexercise.submitted')
}

function registerToAccessAnswerDatabase(event) {
    return register(event,
                    '@@json-register-to-access-answers',
                    'registertoaccessanswerdatabase',
                    'emas.theme.registertoaccessanswerdatabase.submitted')
}

function registerToAskQuestions(event) {
    return register(event,
                    '@@json-register-to-ask-questions',
                    'registertoaskquestions',
                    'emas.theme.registertoaskquestions.submitted')
}

function onServiceRegistered(data, textStatus, jqXHR) {
    jQuery('div#status-message').html(data.message);
    jQuery('div.payservice-form').remove();
}

$(function($) {
    $(".premiumservices-trigger").click(function(){
        $(".premiumservices-panel").toggle("fast");
        $(this).toggleClass("active");
        return false;
    });
});
