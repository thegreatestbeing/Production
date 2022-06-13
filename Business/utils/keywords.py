# Asynchronus Data loading Autocomplete View Function
import json
from csv import reader

from Search.models import Keywords

def collectData():
    with open('static/data.csv', 'r') as data:
        # File = reader(data)
        for keyword in data:
            term    = keyword.strip()
            
            Keywords.objects.create(keyword=term)
        
        print('keywords added !')