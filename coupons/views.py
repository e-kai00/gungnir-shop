from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.utils import timezone
from .models import Coupon
from .forms import ApplyCouponForm


def apply_coupon(request):

    now = timezone.now()

    if request.method == 'POST':
        coupon_form = ApplyCouponForm(request.POST)
        if coupon_form.is_valid():
            code = coupon_form.cleaned_data['code']
            try:
                coupon = Coupon.objects.get(
                    code__iexact=code, 
                    valid_from__lte=now, 
                    expire_on__gte=now, 
                    active=True
                )
                request.session['coupon_id'] = coupon.id
            except Coupon.DoesNotExist:
                request.session['coupon_id'] = None
                messages.info(request, 'This coupon code does not exist.')
                
    else:
        coupon_form = ApplyCouponForm()
    return redirect(reverse('view_basket'))

