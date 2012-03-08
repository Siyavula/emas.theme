jQuery(function($){
    $('a.payservice-overlay').prepOverlay({
        subtype: 'ajax',
        filter: '#content',
        closeselector: '[name=form.button.cancel],[name=form.button.continue]',
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
