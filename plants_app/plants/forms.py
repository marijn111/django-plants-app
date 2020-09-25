from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()
class LoginForm(forms.Form):

    email    = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'input',
        'placeholder': 'Email..'
    }))

    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class': 'input',
        'placeholder': 'Password..'
    }))


class RegisterForm(forms.Form):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'input',
        'placeholder': 'Username..'
    }))

    email = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'input',
        'placeholder': 'Email..'
    }))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class': 'input',
        'placeholder': 'Password..'
    }))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class': 'input',
        'placeholder': 'Repeat Password..'
    }))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username)

        if qs.exists():
            raise forms.ValidationError("Username is taken")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)

        if qs.exists():
            raise forms.ValidationError("Email is already in use!")
        return email

    def clean(self):
        data = self.cleaned_data
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password2 != password:
            raise forms.ValidationError('Passwords must match!')

        return data

