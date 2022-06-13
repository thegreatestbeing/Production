from django.http.response import HttpResponse
from django.shortcuts import render
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import redirect, render

from Inventory.models import Business, Inventory, Relation
from Products.models import Product

from Products.forms import ProductForm


# ajax view function that will create product
def create(request):
    if request.user.is_authenticated:
        if request.method == 'POST':


            return HttpResponse('Created!')
    return render(request, 'products/create.html')

# a
def delete(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            element = request.POST.get('element')

            try: 
                Product.objects.filter(pk=element).delete()
            except:
                pass

            return HttpResponse('deleted!')

    return render(request, 'products/product.html')


def update(request):
    if request.user.is_authenticated:
        # form    = request.method()
        if request.method == 'POST':
            # get all field that is required
            element = request.POST.get('element')
            

            
            try: 
                Product.objects.filter(pk=element).update()
            except:
                pass
            
            return HttpResponse('updated!')
    return render(request, 'products/product.html')


# list all products 
def products(request):
    if request.user.is_authenticated:
        # show products in inventory
        dataset     = []
        data        = [] # 
        label       = [] # products category

        user        = request.user

        relation    = Relation.objects.filter(user=user)

        # for entry in relation:
        business    = Business.objects.filter(relation)
        inventory   = Inventory.objects.filter(business=business)
        products    = Product.objects.filter(inventory=inventory) 
        
        dataset.append({

        })

        return JsonResponse(dataset, safe=False)

