from django.shortcuts import render
from dishes.models import Dish
from restaurants.models import Restaurant

def home(request):
    """
    Home Page View including basic search functionality.
    """
    try:
        query = request.GET.get('q')
    except:
        query = None

    # Ordering all results using restaurant rating
    if query is not None:
        dishes = Dish.objects.filter(name__icontains=query).order_by('-restaurant__rating')
    else:
        query = "Search.."
        dishes = Dish.objects.all().order_by('-restaurant__rating')[:10]

    context = {"dishes":dishes,'query':query}
    return render(request,'base.html',context)