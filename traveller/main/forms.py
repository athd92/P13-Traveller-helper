
from django.contrib.auth.forms import UserCreationForm
from django import forms


class SearchForm(forms.Form):

    search = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'inputForm','placeholder':'Ex: Paris'}), label=False)