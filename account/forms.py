from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(forms.ModelForm):
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', )


    def clean_password2(self):
        clean_data = self.cleaned_data

        if clean_data['password'] != clean_data['password2']:
            raise forms.ValidationError('Passwords don\'t match.')

        return clean_data['password2']

    def clean_email(self):
        clean_data = self.cleaned_data

        try:
            acct = User.objects.get(email=clean_data['email'])
        except Exception as e:
            return clean_data['email']

        raise forms.ValidationError('Email already exist, please try another one.')

        

       
        
        



