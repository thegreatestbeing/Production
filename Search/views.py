from datetime import date, datetime, time, timedelta
from django.contrib.auth import authenticate
from django.http import response
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm

#  model imports
from Inventory.models import Inventory, Relation, Business
from Products.models import Product
from Search.models import Search, Keywords




def collectData(request):
    with open('static/data.csv', 'r') as data:
        # File = reader(data)
        for keyword in data:
            term    = keyword.strip()
            
            Keywords.objects.create(keyword=term)
        
        return HttpResponse('success')



def autocomplete(request, keyword):
    User = request.user
    if request.user.is_authenticated:
        if request.method == 'GET':
            # Term Normalization and filter keywords
            normalized  = keyword.replace("_", " ")
            
            keywords    = Keywords.objects.filter(keyword__startswith=normalized)[:3]
            history     = Search.objects.filter(user=User, history__startswith=normalized)[:6]

            # Dataset
            History     = []
            dataset     = []
        
            # Append Closest match 
            for suggestion in keywords:
                if not Search.objects.filter(user=User, history__startswith=suggestion.keyword).order_by('-timestamp'):
                    
                    dataset.append({
                        'type'      : 'suggestion',
                        'object'    : suggestion.id,
                        'terms'     : suggestion.keyword,
                        'timestamp' : suggestion.timestamp
                    })

            
            # Append History match
            for suggestion in history:
                # for lookup in dataset:

                if suggestion.history not in History:
                    
                    dataset.append({
                        'type'      : 'history',
                        'object'    : suggestion.id,
                        'terms'     : suggestion.history,
                        'timestamp' : suggestion.timestamp
                    })

                    History.append(suggestion.history)

            return JsonResponse(dataset, safe=False)

    return render(request, 'search/search.html')


# Asynchronus Data loading Search View Function
def search(request, keyword):
    if request.user.is_authenticated:
        if request.method == 'GET':
            # Term Normalization and filter keywords
            normalized  = keyword.replace("_", " ")

            # Create history
            Search.objects.create(user=request.user, history=normalized)

            # Dataset
            dataset = []


            # Search for Products
            Product.objects.filter()[:10]

            dataset.append({
                'request'   : 'search',
                'query'     : normalized
            })

            print(dataset)
                 
            return JsonResponse(dataset, safe=False)

    return render(request, 'search/search.html')


def history(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            action  = request.POST.get('action')
            element = request.POST.get('element')
            type    = request.POST.get('type')

            if type == 'history':
                Search.objects.filter(pk=element).delete()

            return HttpResponse('Success!')
    return render(request, 'search/search.html')

