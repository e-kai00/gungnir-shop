from django.shortcuts import render, redirect, reverse
from .forms import ShippingForm


def shipping_options(request):   

    if request.method == 'POST':
        shipping_form = ShippingForm(request.POST)
        if shipping_form.is_valid():
            shipping = shipping_form.cleaned_data['shipping']
            # shipping_price = shipping_option.price
            # shipping_method = shipping_option.method
            request.session['shipping_id'] = shipping.id
    else:
        shipping_form = ShippingForm()
        
    return redirect(reverse('view_basket'))
    