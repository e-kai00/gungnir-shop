from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import UserProfileForm
from checkout.models import Order


@login_required
def profile(request):
    """
    View and update user profile. Display
    user's order history.
    """

    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated succsessfully.')
        else:
            messages.error(request, 'Update failed. Please ensure the form is valid.')
    else: 
        form = UserProfileForm(instance=profile)

    orders = profile.orders.all()

    template = 'profiles/profile.html'
    context = {
        'form': form,
        'orders': orders,
        'on_profile_page': True,
    }
    return render(request, template, context)


def order_history(request, order_number):
    """ Display details of specific order in user's order history """

    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, f'This order has been made on {order.date.strftime("%d %b %Y")}')

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }
    return render(request, template, context)



