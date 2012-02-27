jQuery(function($){
    $('a.payservice-overlay').prepOverlay({
        subtype: 'ajax',
        filter: '#content',
        closeselector: '[name=form.button.cancel]',
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
    jQuery.ajax({
        url: '@@register-for-more-exercise',
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
    //event.preventDefault();

}
