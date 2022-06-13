from datetime import date, datetime, timedelta
from django.contrib.auth import authenticate
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm


from Account.forms import SignupForm
from Inventory.forms import DetailForm, BusinessForm
from Products.forms import ProductForm

from Inventory.models import Inventory, Relation, Business
from Products.models import Product


# render inventory in one page.
def inventory(request):
    if request.user.is_authenticated:
        # show products in inventory
        relation    = Relation.objects.filter(user=request.user)
        

        for entry in relation:
            print({entry.business, entry.user, entry.role})
            business    = Business.objects.filter(id=entry.business.id)
            inventory   = Inventory.objects.filter(business=business)
            products    = Product.objects.filter(inventory=inventory)

            
        # forms if manager or owener

        if request.method == 'POST':
            business_form   = BusinessForm(request.POST)
            detail_form     = DetailForm(request.POST)
            product_form    = ProductForm(request.POST)  

            if business_form.is_valid():
                business_form.save()
                return redirect('/')

            if detail_form.is_valid():
                detail_form.save()
                return redirect('/')

            if product_form.is_valid():
                product_form.save()
                return redirect('/')

        else:
            business_form   = BusinessForm()
            detail_form     = DetailForm()
            product_form    = ProductForm()  
    
        return render(request, 'inventory/home.html', {
            # 'inventory'     : inventory,
            # 'products'      : products,
            # 'business'      : business,
            'business_form' : business_form,
            'detail_form'   : detail_form,
            'product_form'  : product_form
        })

    elif not request.user.is_authenticated:
        login   = AuthenticationForm()
        signup  = SignupForm()

        if request.method == 'POST':
            login   = AuthenticationForm(request.POST or None)
            signup  = SignupForm(request.POST)

            if login.is_valid():
                username    = login.cleaned_data.get("username")
                password    = login.cleaned_data.get("password")

                user        = authenticate(request, username=username, password=password)

                return redirect('/')
            elif signup.is_valid(): 
                signup.save()

                return redirect('/')

        return render(request, 'account/access.html', {
            'login'     : login,
            'signup'    : signup
        })



# def updateProduct(request, pk):


def sales(request):
    pass
    # if request.user.is_authenticated:
    #     user        = request.user
    #     week        = (datetime.now() - timedelta(days=6)).date() 

    #     # datasets for sales revanue of the day, month, and year
    #     labels      = []
    #     data        = []


    #     # get the business id and extract Sales of the all time
    #     relation    = Relation.objects.filter(user=request.user)

    #     for object in relation:
    #         # business    = Business.objects.filter(id=object.business.id)
    #         # queryset    = Sale.objects.filter(saler=business).filter(timestamp=week)

    #         daily_sales = 


    #         for query in queryset:
    #             # monthly sales | weekly sales | daily sales        
                
    #             data.append({
    #                 ''   : ,
    #             })

    #     # get the net profit 


def Invoice(request):
    pass



