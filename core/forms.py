from django import forms
from .models import EmployeeList
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


def apply_custom_styles(field):
    field.widget.attrs.update({
        'class': 'bg-white rounded-full placeholder-gray-900 shadow appearance-none border rounded w-full py-2 px-3 text-black leading-tight focus:outline-none focus:shadow-outline hover:placeholder-gray-300 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'
    })

def apply_custom_styles_Login(field):
    field.widget.attrs.update({
        'class': 'bg-white rounded-full placeholder-gray-900 shadow appearance-none border rounded w-full py-2 px-3 text-black leading-tight focus:outline-none focus:shadow-outline hover:placeholder-gray-300'  # Change 'blue' to any color you prefer
    })


class EditForm(forms.ModelForm):
    class Meta:
        model = EmployeeList
        fields = ['name', 'job', 'favorite_color']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].required = False
        self.fields['job'].required = False
        self.fields['favorite_color'].required = False
        
        for field in self.fields:
            apply_custom_styles(self.fields[field])


        
class AddDataForm(forms.ModelForm):
    class Meta:
        model = EmployeeList
        fields = ['name', 'job', 'favorite_color']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].required = True
        self.fields['job'].required = True
        self.fields['favorite_color'].required = False

        for field in self.fields:
                apply_custom_styles(self.fields[field])


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2", "email",]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            apply_custom_styles_Login(self.fields[field])
  

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].required = True
        self.fields['password'].required = True

        apply_custom_styles_Login(self.fields['username'])
        apply_custom_styles_Login(self.fields['password'])




