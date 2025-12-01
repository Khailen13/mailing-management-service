from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class UserRegisterForm(UserCreationForm):
    email = forms.CharField(max_length=50, required=True)

    class Meta:
        model = User
        fields = ("email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        fields_placeholders = {
            "email": "Введите адрес эл. почты",
            "password1": "Введите пароль",
            "password2": "",
        }
        for field, placeholder in fields_placeholders.items():
            self.fields[field].widget.attrs.update({"class": "form-control", "placeholder": placeholder})


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email", "avatar", "phone_number", "country")

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        fields_placeholders = {
            "email": "Введите адрес эл. почты",
            "avatar": "",
            "phone_number": "Введите номер телефона",
            "country": "Укажите страну",
        }
        for field, placeholder in fields_placeholders.items():
            self.fields[field].widget.attrs.update({"class": "form-control", "placeholder": placeholder})
