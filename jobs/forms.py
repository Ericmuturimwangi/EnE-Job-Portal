from django import forms
from .models import Job, Application
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'location', 'job_type']

# class ApplicationForm(forms.ModelForm):
#     class Meta:
#         model = Application
#         fields = ['cover_letter', 'resume']
        
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']