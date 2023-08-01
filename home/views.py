from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from products.models import Product, Category


def index(request):

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

    current_sorting = f'{sort}_{direction}'

    announcement = get_announcement()

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
        'announcement': announcement
    }
                

    return render(request, 'home/index.html', context)


def get_announcement():

    try:
        with open("data/announcement.txt", "r") as file:
            return file.read()
    except FileNotFoundError:
        return "No announcement found."
    

def update_announcement(new):

    with open("data/announcement.txt", "w") as file:
            return file.write(new)
    

def announcement(request):

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

    
 