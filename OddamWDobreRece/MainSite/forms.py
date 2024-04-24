from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from .models import Donation


class AddUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Potwierdź hasło", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password != password_confirm:
            raise ValidationError("Hasła nie pasują do siebie. Upewnij się, że wprowadzone hasła są takie same.")
        return cleaned_data
    

class LoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('email')
        password = cleaned_data.get('password')
        self.user = authenticate(username=username, password=password)
        if self.user is None:
            raise ValidationError("Wrong login or pass")
        

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['quantity',
                  'institution',
                  'address',
                  'phone_number',
                  'donation_city', 
                  'zip_code',
                  'pick_up_date',
                  'pick_up_time',
                  'pick_up_comment',
                  'user']
