from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings
from django.db.models import Q
from django.db.models.functions import Lower
from products.models import Product, Category
import os


def index(request):
    """ View all products. Sort and search queries """

    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

        # filter by category
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        # search site
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(
                    request,
                    "You didn't eneter any search criteria!"
                )
                return redirect(reverse('home'))

            queries = (Q(name__icontains=query) |
                       Q(description__icontains=query))
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    announcement = get_announcement()

    template = 'home/index.html'
    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
        'announcement': announcement
    }

    return render(request, template, context)


def get_announcement():
    """  Retrieve text announcement from announcement.txt file """

    announcement_path = (
        os.path.join(settings.STATICFILES_DIRS[0], 'data', 'announcement.txt')
    )

    try:
        with open(announcement_path, "r") as file:
            return file.read()
    except FileNotFoundError:
        return "No announcement found."


def update_announcement(new):
    """ Update the announcement with the given text and save it to a file """

    announcement_path = (
        os.path.join(settings.STATICFILES_DIRS[0], 'data', 'announcement.txt')
    )

    with open(announcement_path, "w") as file:
        return file.write(new)


def announcement(request):
    """
    Update and display announcement on home page.
    If the user is not a superuser (shop owner), they will be redirected
    to the home page.
    """

    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only shop owner can do this.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        new = request.POST.get('announcement', '')
        update_announcement(new)
        messages.success(request, 'Announcement has been updated.')
        return redirect(reverse('home'))

    announcement = get_announcement()

    template = 'home/announcement.html'
    context = {
        'announcement': announcement
    }

    return render(request, template, context)
