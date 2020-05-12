
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SearchForm(forms.Form):
    '''Form used for general query'''
    search = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'inputForm','placeholder':'Ex: Paris'}), label=False)


class UserFormWithEmail(UserCreationForm):
    '''Class used to register with email'''

    email = forms.EmailField(required=True)
    age = forms.DecimalField(max_digits=2, min_value=18, decimal_places=0)
    
    def __init__(self, *args, **kwargs):
        super(UserFormWithEmail, self).__init__(*args, **kwargs)

        for fieldname in ["username", "email", "password1", "password2"]:
            self.fields[fieldname].help_text = None

    def save(self, commit=True):
        user = super(UserFormWithEmail, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user