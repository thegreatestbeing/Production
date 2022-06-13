from django import forms

# models import
class AutocompleteForm(forms.Form):
    keyword = forms.CharField(label='keyword', max_length=256)

class SearchForm(forms.Form):
    keyword = forms.CharField(label='keyword', max_length=256)

class HistoryForm(forms.Form):
    object  = forms.IntegerField(label='object')