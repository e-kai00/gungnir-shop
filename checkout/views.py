from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from .forms import OrderForm
from .models import Order, OrderLineItem
from products.models import Product
from profiles.models import UserProfile
from profiles.forms import UserProfileForm
from basket.contexts import basket_contents
from coupons.models import Coupon
from shipping.models import Shipping
import stripe

# send confirmation email
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


def checkout(request):
    """
    Handle checkout process for user's shopping basket
    and save order to database.
    It retrieves user's shopping basket, shipping_id,
    and coupon_id from the session, and creates order.
    If default delivery information exists, it is used
    to pre-fill order form.
    """

    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    
    if request.method == 'POST':
        basket = request.session.get('basket', {})
        coupon_id = request.session.get('coupon_id')
        coupon = None
        try:
            if coupon_id:
                coupon = Coupon.objects.get(id=coupon_id)
            else:
                coupon_id = None
        except ObjectDoesNotExist:
            coupon_id = None

        shipping_id = request.session.get('shipping_id')
        shipping = None        
        default_shipping = None
        try:
            if shipping_id is not None:
                shipping = Shipping.objects.get(id=shipping_id)                    
            else:
                default_shipping = Shipping.objects.first() if Shipping.objects.exists() else None            
        except ObjectDoesNotExist:
            default_shipping = Shipping.objects.first() if Shipping.objects.exists() else None        

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
        if order_form.is_valid():
            order = order_form.save(commit=False)

            if shipping:
                order.shipping = shipping
                order.shipping_cost = shipping.price
            else:
                order.shipping = default_shipping
                order.shipping_cost = default_shipping.price

            if coupon:
                order.coupon = coupon
                order.discount = coupon.value
            order.save()
            if coupon: 
                del request.session['coupon_id']
            
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
        else:
            messages.error(request, 'There was an error with your form. \
                           Please, check your information once again.')
    
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

    # use default delivery info to pre-fill the form
    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user)
            order_form = OrderForm(initial={
                'full_name': profile.user.get_full_name(),
                'email': profile.user.email,
                'phone_number': profile.default_phone_number,
                'country': profile.default_country,
                'postcode': profile.default_postcode,
                'town_or_city': profile.default_town_or_city,
                'street_address1': profile.default_street_address1,
                'street_address2': profile.default_street_address2,
                'county': profile.default_county,
            })
        except UserProfile.DoesNotExist:
            order_form = OrderForm()

    else:
        order_form = OrderForm()

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }
    return render(request, template, context)


def send_confirmation_email(order):
    """ Send confirmation email once order completed """

    customer_email = order.email
    subject = render_to_string(
        'checkout/confirmation_emails/confirmation_email_subject.txt',
        {'order': order}
    )
    body = render_to_string(
        'checkout/confirmation_emails/confirmation_email_body.txt',
        {'order': order, 'contact email': settings.DEFAULT_FROM_EMAIL}
    )
    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [customer_email]
    )


def checkout_success(request, order_number):
    """
    Checkout success page.
    Retrieves order associated with given order number and 
    attaches it to the user's profile if user is authenticated. 
    If 'save info' option was checked during checkout,
    updates user's profile with order's delivery information.
    Sends order confirmation email.
    """

    save_info = request.session.get('save-info')
    order = get_object_or_404(Order, order_number=order_number)
    
    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)        
        order.user_profile = profile
        order.save()

    # if 'save info' checked
    if save_info:
        profile_data = {
            'default_phone_number': order.phone_number,
            'default_country': order.country,
            'default_postcode': order.postcode,
            'default_town_or_city': order.town_or_city,
            'default_street_address1': order.street_address1,
            'default_street_address2': order.street_address2,
            'default_county': order.county,
        }
        # create instance of user profile form and populate it with profile data obtained
        user_profile_form = UserProfileForm(profile_data, instance=profile)
        if user_profile_form.is_valid():
            user_profile_form.save()

    messages.success(request, f"Your order has been processed successfully! \
                     Your order number is {order_number}. Keep an eye on \
                     your inbox, as we'll be sending a confirmation to {order.email}.")

    if 'basket' in request.session:
        del request.session['basket']

    send_confirmation_email(order)

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }
    return render(request, template, context)


