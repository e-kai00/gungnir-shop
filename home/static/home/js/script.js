$(document).ready(function(){
    // Bootstrap
    $('.dropdown-toggle').dropdown();


    // product card border on hover
    $('.card').hover(
        function(){
            $(this).removeClass('border-0').addClass('border');
        },
        function(){
            $(this).removeClass('border').addClass('border-0');
        }
    );


    // sort products 
    $('#sort-selector').change(function() {
        var selector = $(this);
        var currentUrl = new URL(window.location);
        var selectedVal = selector.val();

        if (selectedVal != "reset") {
            var sort = selectedVal.split("_")[0];
            var direction = selectedVal.split("_")[1];

            currentUrl.searchParams.set("sort", sort);
            currentUrl.searchParams.set("direction", direction);
            window.location.replace(currentUrl);

        } else {
            currentUrl.searchParams.delete("sort");
            currentUrl.searchParams.delete("direction");
            window.location.replace(currentUrl);
        }
    });


    // scroll-to-top button
    $(window).scroll(function(){
        if ($(this).scrollTop() > 300) {
            $('.btt-button').css('display', 'block');
        } else {
            $('.btt-button').css('display', 'none');
        }
    });

    $('.btt-button').click(function() {
        $("html, body").animate({ scrollTop: 0 }, "slow");
    });     
    
    
    // last updated on - announcement section
    function displayDate() {
        const lastUpdate = localStorage.getItem('lastUpdated');
        const updateField = $('#last-update');
        if (lastUpdate) {
            updateField.text(lastUpdate)
        }
    };

    displayDate();

});