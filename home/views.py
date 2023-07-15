from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from products.models import Product, Category


def index(request):

    products = Product.objects.all()
    query = None
    categories = None

    if request.GET:
        # filter by category
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            # display caregory name for user
            categories = Category.objects.filter(name__in=categories)


        # search site 
        if 'q' in request.GET:            
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't eneter any search criteria!")
                return redirect(reverse('home'))
            
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories
    }
                

    return render(request, 'home/index.html', context)

 