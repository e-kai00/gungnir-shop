from django.shortcuts import redirect, reverse
from .forms import ShippingForm


def shipping_options(request):
    """
    Set selected shipping option for the current user's session.
    If request method is POST, it validates submitted
    shipping option from form. If form is valid, it sets
    'shipping_id' key in the request session to the ID of selected shipping.
    If request method is GET, it displays ShippingForm to allow
    to select shipping option.
    """

    if request.method == 'POST':
        shipping_form = ShippingForm(request.POST)
        if shipping_form.is_valid():
            shipping = shipping_form.cleaned_data['shipping']
            request.session['shipping_id'] = shipping.id
    else:
        shipping_form = ShippingForm()

    return redirect(reverse('view_basket'))
