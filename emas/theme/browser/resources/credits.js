jQuery(function($){
    $('a.credit-overlay').prepOverlay({
        subtype: 'ajax',
        filter: '#content',
        closeselector: '[name=form.button.cancel]',
        formselector: '#credit-buy-form',
        config: {
            onClose : function (e) {
                var p = this.getOverlay();
                /* If there is no form within the overlay, reload */
                if($('#credit-buy-form', p).length == 0){
                    location.reload();
                }
            }
        }

    });
});
