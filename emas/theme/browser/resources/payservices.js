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

function buyCredits(event) {
    event.preventDefault();
    element = jQuery('input#credits-to-buy');
    var amount = parseInt(jq(element).attr('value'));
    if (isNaN(amount)) {
        alert("'" + jq(element).attr('value') + "' is not a valid number!");
        jq(element).attr('value', 0);
        return false;
    }
    jQuery.ajax({
        url: '@@json-buycredits',
        dataType: 'json',
        data: {'buy': amount},
        success: onCreditsBought,
        error: errorHandler,
    });
}

function onCreditsBought(data, textStatus, jqXHR) {
    jQuery('div#status-message').html(data.message);
    jQuery('span.credit-value').html(data.credits);
    var url = jQuery('input#view_url').val();
    jQuery.ajax({
        url: url,
        success: updateOverlay,
        error: errorHandler,
    });
}

function updateOverlay(data, textStatus, jqXHR) {
    var element = jQuery('div.payservice-form');
    var doc = jQuery(data);
    var content = jQuery(doc).find('div.payservice-form');
    jQuery(element).replaceWith(content);
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

function register(event, url, fieldname, formtoken) {
    event.preventDefault();
    var data = new Object();
    data[fieldname] = 'on';
    data[formtoken] = 'submitted';
    jQuery.ajax({
        url: url,
        dataType: 'json',
        data: data,
        success: onServiceRegistered,
        error: errorHandler,
    });
}

function onServiceRegistered(data, textStatus, jqXHR) {
    jQuery('div#status-message').html(data.message);
    jQuery('div.payservice-form').remove();
}
