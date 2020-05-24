
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


# Create your models here.
class PostForm(forms.Form):
    """
    Class used to define a post
    """
    country = forms.CharField(max_length=200)
    city = forms.CharField(max_length=200)
    total = forms.DecimalField(max_digits=4, decimal_places=0)
    wanted = forms.DecimalField(max_digits=4, decimal_places=0)
    free = forms.DecimalField(max_digits=4, decimal_places=0)
    interest = forms.CharField(max_length=200)
    title = forms.CharField(max_length=200)
    message = forms.CharField(max_length=2000)
    start = forms.CharField(max_length=200)
    end = forms.CharField(max_length=200)
    budget = forms.CharField(max_length=100)

    def save(self, commit=True):

        country = self.country.cleaned_data['country']
        city = self.city.cleaned_data['city']
        total = self.total.cleaned_data['total']
        wanted = self.wanted.cleaned_data['wanted']
        free = self.free.cleaned_data['free']
        interest = self.interest.cleaned_data['interest']
        title = self.title.cleaned_data['title']
        message = self.message.cleaned_data['message']
        start = self.start.cleaned_data['start']
        end = self.end.cleaned_data['end']
        budget = self.budget.cleaned_data['budget']
        
        return self.country

    def __repr__(self):
        return f"{self.country}"