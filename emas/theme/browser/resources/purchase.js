function calctotal() {
    var totalcost = 0;
    var items = $('input.quantity');
    for (var count = 0; count < items.length; count++) {
        item = items[count];
        quantity = parseInt($(item).val(), 10);
        if (isNaN(quantity)){
            quantity = 0;
            $(item).val('');
        }
        price = parseInt($(item).attr('price'), 10);
        totalcost = totalcost + (quantity * price);
    }
    $('#totalcost').html("R"+totalcost);
}

jQuery(document).ready(function() {
    calctotal();

    $("#selectitems input").change(calctotal);

    $("#selectitems button[type='submit']").click(function () {
        result = true;

        if ($('#totalcost').html() == "R0") {
            alert('You have to order something before you can continue');
            result = false;
        }

        return result;
    });
});
