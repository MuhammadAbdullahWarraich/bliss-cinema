from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignupForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ['username', 'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class ShowtimeSearchForm(forms.Form):
    date = forms.DateField(label='date', widget=forms.DateInput(attrs={'type': 'date'}))

class BookShowtimeForm(forms.Form):
    showtime_id = forms.IntegerField()
    num_tickets = forms.IntegerField()