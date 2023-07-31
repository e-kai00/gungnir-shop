from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from decimal import Decimal
from django.shortcuts import get_object_or_404
from products.models import Product
from coupons.models import Coupon
from shipping.models import Shipping
from coupons.forms import ApplyCouponForm
from shipping.forms import ShippingForm



def basket_contents(request):

    # basket items
    basket_items = []
    total = 0 
    product_count = 0
    basket = request.session.get('basket', {})
    
    for item_id, quantity in basket.items():
        product = get_object_or_404(Product, pk=item_id)
        total += quantity * product.price
        product_count += quantity
        basket_items.append({
            'item_id': item_id,
            'quantity': quantity,
            'product': product
        })

    # if total < settings.FREE_DELIVERY_THRESHOLD:
    #     delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100) 
    #     free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total        
    # else:
    #     delivery = 0
    #     free_delivery_delta = 0

    # shipping
    shipping_form = ShippingForm()
    shipping_id = request.session.get('shipping_id')    
    try:
        if shipping_id is not None:
            shipping = Shipping.objects.get(id=shipping_id)
            shipping_cost = shipping.price
        else:
            shipping = None
            shipping_cost = 0
    except ObjectDoesNotExist:
        shipping = None
        shipping_cost = 0

    # coupon
    apply_coupon_form = ApplyCouponForm()
    coupon_id = request.session.get('coupon_id')
    try:        
        if coupon_id:
            coupon = Coupon.objects.get(id=coupon_id)
            discount = total * (coupon.value / Decimal(100))
            total_with_coupon = total - discount        
            grand_total = shipping_cost + total_with_coupon
        else:
            coupon = None
            discount = 0
            grand_total = shipping_cost + total + discount
    except ObjectDoesNotExist:
            coupon = None
            discount = 0
            grand_total = shipping_cost + total + discount    
    
    
    context = {
        'basket_items': basket_items,
        'total': total,
        'product_count': product_count,
        'delivery': shipping_cost,
        # 'free_delivery_delta': free_delivery_delta,
        # 'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'coupon': coupon,
        'discount': discount,        
        'apply_coupon_form': apply_coupon_form,
        'grand_total': grand_total,     
        'shipping_form': shipping_form,
    }

    return context