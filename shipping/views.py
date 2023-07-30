from django.shortcuts import render, redirect, reverse
from .forms import ShippingForm


def shipping_options(request):   

    if request.method == 'POST':
        shipping_form = ShippingForm(request.POST)
        if shipping_form.is_valid():
            shipping_option = shipping_form.cleaned_data['shipping']
            shipping_price = shipping_option.price
            shipping_method = shipping_option.method
        return redirect(reverse('view_basket'))
    else:
        shipping_form = ShippingForm()

    template = 'shipping/shipping.html'
    
    context = {
        'shipping_form': shipping_form,               
    }

    return render(request, template, context)
    