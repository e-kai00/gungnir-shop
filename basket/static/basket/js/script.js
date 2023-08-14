// display shipping method chosen by user        
function setSelectedMethod(method) {
    sessionStorage.setItem('shippingMethod', method);
}

$(document).ready(function () {
    function displayMethod() {
        const selectedMethod = sessionStorage.getItem('shippingMethod');
        const method = $('#id_shipping');
        if (selectedMethod) {
            method.val(selectedMethod);
        }
    }

    $('#shipping-form').submit(function () {
        const methodValue = $('#id_shipping').val();
        setSelectedMethod(methodValue);
    });

    displayMethod();


    // scroll-to-top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 300) {
            $('.btt-button').css('display', 'block');
        } else {
            $('.btt-button').css('display', 'none');
        }
    });

    $('.btt-button').click(function () {
        $("html, body").animate({ scrollTop: 0 }, "slow");
    });

});