from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Curriculum, JobPosition, JobApply
from django.forms.widgets import PasswordInput

class RegisterForm(UserCreationForm): #works
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    date_of_birth = forms.DateField(required=False, help_text="YYYY-MM-DD")
    is_seeker = forms.BooleanField(required=False, help_text="Registering to seek employees? Tick this!")
    company_name = forms.CharField(required=False, max_length=200, help_text="Company Name")
    creg_number = forms.CharField(required=False, max_length=8, help_text="Company Serial Number")
   
    class Meta:
        model = User
        fields = ['username']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)

class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=65, required=True)
    email = forms.EmailField(required=False)
    class Meta:
        model = User
        fields = ['username', 'email']

  

class UserProfileEdit(forms.ModelForm): #edit only User fields and UserProfile jobless field
    class Meta:
        model = UserProfile
        fields = [
            "first_name",
            "last_name",
            "email",
            "date_of_birth",   
        ]

class SeekerProfileEdit(forms.ModelForm): #edit only User fields and UserProfile jobless fields
    class Meta:
        model = UserProfile
        fields = [
            "first_name",
            "last_name",
            "email",
            "date_of_birth", 
            "company_name", 
            "creg_number",
            "company_descript",
        ]     


class CurriculumForm(forms.ModelForm):
    class Meta:
        model = Curriculum
        fields = [
            "cv_education",
            "cv_career",
            "cv_skills",
            "cv_other",
        ]


class JobPositionForm(forms.ModelForm):
    class Meta:
        model = JobPosition
        fields = [
            "job_title",
            "job_desc",
            "job_field",
            "job_skills",
            "published",
        ] 

class MotivationForm(forms.ModelForm):
    class Meta:
        model = JobApply
        fields = ["motivation"]


