from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings
from .forms import OrderForm
from .models import Order, OrderLineItem
from products.models import Product
from basket.contexts import basket_contents
import stripe


def checkout(request):

    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY    

    # post method
    if request.method == 'POST':
        basket = request.session.get('basket', {})
        form_data = {            
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }
        order_form = OrderForm(form_data)
        # if form valid
        if order_form.is_valid():
            order = order_form.save()
            for item_id, quantity in basket.items():
                try:
                    product = Product.objects.get(id=item_id)
                    order_line_item = OrderLineItem(
                        order=order,
                        product=product,
                        quantity=quantity
                    )
                    order_line_item.save()
                except Product.DoesNotExist:
                    messages.error(request, 'One of the product in your basket was not found.')
                    order.delete()
                    return redirect(reverse('view_basket'))
            request.session['save-info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success', args=[order.order_number]))
        # if form not valid
        else:
            messages.error(request, 'There was an error with your form. \
                           Please, check your information once again.')
    # get method
    else:
        basket = request.session.get('basket', {})
        if not basket:
            messages.error(request, "Your basket is empty")
            return redirect(reverse('home'))

        current_basket = basket_contents(request)
        total = current_basket['grand_total']
        stripe_total = round(total *100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing.')

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)
