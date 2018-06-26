from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Customer


class ExecutiveSignUpForm(UserCreationForm):
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
    bio=forms.CharField(help_text='Write Bio ',max_length=200)
    location=forms.CharField(help_text="Enter city",max_length=100)
    admin=forms.BooleanField(help_text="Admin Account",required=False)
    class Meta:
        model = User
        fields = ('admin','username','email', 'birth_date','bio','location','password1', 'password2', )


class CustomerSignUpForm(forms.ModelForm):
  class Meta:
        model = Customer
        fields = ('first_name','last_name' )