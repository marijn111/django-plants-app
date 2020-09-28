from django import forms
from django.contrib.auth import get_user_model

import datetime
import pytz

utc=pytz.UTC


STANDPLACE_CHOICES = [
    ('sun', 'Direct Sunlight'),
    ('light', 'Indirect Sunlight'),
    ('shadow', 'Shadow'),
    ('any', "Doesn't matter")
]


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


class AddPlantForm(forms.Form):

    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'input',
        'placeholder': 'Name of your plant bro'
    }))

    description = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'textarea',
        'placeholder': 'Say something about your plant bro...',
        'rows': 3
    }))

    age = forms.DateTimeField(widget=forms.DateInput(attrs={
        'type': 'date'
    }))

    image = forms.FileField(required=False,widget=forms.FileInput(attrs={
        'class': 'file-input'
    }))

    watering = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'How much water does your plant need bro?',
        'class': 'textarea',
        'rows': 3
    }))

    standplace = forms.CharField(widget=forms.Select(choices=STANDPLACE_CHOICES))

    def clean_age(self):
        plant_age = self.cleaned_data.get('age')
        now = datetime.datetime.now()
        now = now.replace(tzinfo=utc)

        if plant_age > now:
            raise forms.ValidationError("Your plant can not be from the future bro...")
        return plant_age

    def clean_image(self):
        image = self.cleaned_data.get('image', None)
        if not image:
            # do some validation, if it fails
            raise forms.ValidationError('epic image fail')
        return image



