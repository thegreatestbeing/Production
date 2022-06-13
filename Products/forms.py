from django import forms

# model imports
from Products.models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model   = Product
        fields  = ('name', 'description', 'inventory')
