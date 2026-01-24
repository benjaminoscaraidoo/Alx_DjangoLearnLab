
from django import forms


class ExampleForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)


class SearchForm(forms.Form):
    query = forms.CharField(required=False, max_length=100)
