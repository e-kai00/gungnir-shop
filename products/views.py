from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Product, Reviews
from .forms import ProductForm


def product_detail(request, product_id):
    """ View single product details """

    product = get_object_or_404(Product, pk=product_id)

    template = 'products/product_detail.html'
    context = {
        'product': product,
    }
    return render(request, template, context)


@login_required
def add_product(request):
    """ View for adding new product to the shop """

    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only shop owner can do this.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Product added.')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(
                request,
                'Failed to add product. Please ensure the form is valid.'
            )
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
    }
    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """ View for editing an existing product """

    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only shop owner can do this.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated.')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(
                request,
                'Failed to update product. Please ensure the form is valid.'
            )
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }
    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """ View for deleting a product """

    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only shop owner can do this.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted.')
    return redirect(reverse('home'))


def submit_review(request, product_id):
    """
    View for submitting or updating product review.
    Checks if user has already submitted review for the product.
    If review exists, it updates existing review. If no review
    exists, it creates new review.
    Checks if user submitted rating. If rating submitted, it
    updates review or creates new review. If no rating is submitted,
    it displays an error message.
    """

    if not request.user.is_authenticated:
        return redirect(reverse('account_login'))

    user = request.user
    product = get_object_or_404(Product, pk=product_id)
    review = Reviews.objects.filter(created_by=user, product=product).first()

    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('review', '')

        if rating is None:
            messages.error(
                request,
                'Please provide star rating before submitting your review.'
            )
            return redirect(reverse('product_detail', args=[product_id]))

        if review:
            review.rating = rating
            review.comment = comment
            review.save()
            messages.success(request, 'Your feedback has been updated.')

        else:
            Reviews.objects.create(
                product=product,
                comment=comment,
                rating=rating,
                created_by=user
            )
            messages.success(request, 'Thank you for your feedback!')

        return redirect(reverse('product_detail', args=[product_id]))

    template = 'products/product_detail.html'
    context = {
        'product': product,
    }
    return render(request, template, context)
