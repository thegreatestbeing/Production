from PIL import Image

from django import forms
from django.core.files import File
from django.db.models import fields


from Inventory.models import Contact, Detail, Business, Timing
from Products.models import Category, Product, Price
from Revenue.models import Invoice

class BusinessForm(forms.ModelForm):
    class Meta:
        model   = Business
        fields  = ('name',)


class DetailForm(forms.ModelForm):
    class Meta:
        model   = Detail
        fields  = ('address', 'description', 'business')


class ContactForm(forms.ModelForm):
    class Meta:
        model   = Contact
        fields  = ('email', 'contact', 'business')



class PriceForm(forms.ModelForm):
    class Meta:
        model   = Price
        fields  = ('product', 'wholesale', 'retail')


class InvoiceForm(forms.ModelForm):
    class Meta:
        model   = Invoice
        fields  = ('buyer', 'saler', 'product', 'discount', 'tax', 'total')


class TimingForm(forms.ModelForm):
    class Meta:
        model   = Timing
        fields  = ('weekday', 'opening', 'closing', 'business')


# Extras functions 

# class ReturnForm(forms.ModelForm):
#     class Meta:
#         model   = Return
#         fields  = ()