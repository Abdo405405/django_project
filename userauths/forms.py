from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm 
from userauths.models import User 
from datetime import date
import re
pattern = r"^[A-Za-z\s'-]+$"## this is condtions to validate names in regestration form 
regex=re.compile(pattern)   ##   
class User_Register_Form (forms.ModelForm): # if you use UserCreationForm inhertiance it will give you fields auto in form
    username=forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Name of Account","hx-get":"/hide_error_messages/" ,"hx-trigger":"input", "hx-target":"#hide_error_messages4"  }))  
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter First Name',"hx-get":"/hide_error_messages/" ,"hx-trigger":"input", "hx-target":"#hide_error_messages1"   })
    )
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter Last Name', "hx-get":"/hide_error_messages/" ,"hx-get":"/hide_error_messages/" ,"hx-trigger":"input", "hx-target":"#hide_error_messages2"})
    )
    password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder' :"Must be bigger than 8","hx-get":"/hide_error_messages/" ,"hx-trigger":"input", "hx-target":"#hide_error_messages5"}))
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'It should be like a password',"hx-get":"/hide_error_messages/" ,"hx-trigger":"input", "hx-target":"#hide_error_messages6"}),required=True
    )
    gender = forms.ChoiceField(
    choices=[("",""),('male', 'Male'), ('female', 'Female',)],
    widget=forms.Select(attrs={"hx-get":"/hide_error_messages/" ,"hx-trigger":"input", "hx-target":"#hide_error_messages8"})
    )
    birthday = forms.DateField(widget=forms.DateInput(attrs={'type': 'date',"hx-get":"/hide_error_messages/" ,"hx-trigger":"input", "hx-target":"#hide_error_messages7"}), required=True)
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Enter Email',"hx-get":"/hide_error_messages/" ,"hx-trigger":"input", "hx-target":"#hide_error_messages3"}),required =True
    )
    class Meta :   # Captial not small to avoid error take care 
        model = User
        fields = ["username", "email", "password", "first_name", "last_name", "confirm_password", "gender", "birthday"]
        # error_messages={
        #     "email" :{"unique":"The Account is Already Exist"},  If You want To Edit Error Massage 
        #     "username":{"       "}
        # }


    def clean(self):
        cleaned_data= super().clean()  #  clean() method of the forms.ModelForm class handles basic validation and cleaning of individual form fields. It checks things like required fields, data types, and other basic validation rules defined in the model field definitions (e.g., max_length, blank, null, etc.).
        pass1=cleaned_data.get("password")
        pass2=cleaned_data.get("confirm_password")
        birthday=cleaned_data.get("birthday")
        first_name=cleaned_data.get("first_name")
        last_name=cleaned_data.get("last_name")
        print(last_name)
        if first_name:
            if not regex.match(first_name)and first_name:
                self.add_error("first_name","Please enter a valid name")
        if last_name:
            if  not regex.match(last_name) and last_name!=None:
                 self.add_error("last_name","Please enter a valid name")
        if birthday and birthday > date.today():
            self.add_error("birthday","Please enter a valid birthdate")
        if pass1:
            if len(pass1)<8 :
                self.add_error("password","A password must be greater than 8  characters ")
        if (pass1 and pass2) and pass1!=pass2:
            self.add_error("confirm_password","Passwords do not match.")
        elif not pass1 and pass2:
            self.add_error("confirm_password","👈First Enter a Password")
        return cleaned_data