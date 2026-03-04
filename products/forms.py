from django import forms
from django.contrib.auth.models import User


class RegisterUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "username", "password"]

    password_repeat = forms.CharField(
        label="Confirmar Senha", widget=forms.PasswordInput()
    )
    password = forms.CharField(widget=forms.PasswordInput(), label="Senha")
    email = forms.EmailField(label="Email")
    username = forms.CharField(label="Nome")

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        password_repeat = cleaned_data.get("password_repeat")

        if password != password_repeat:
            raise forms.ValidationError("Senhas devem ser iguais.")

        return cleaned_data

    def clean_email(self):
        new_email = self.cleaned_data.get("email", "")
        exists = User.objects.filter(email=new_email).exists()

        if exists:
            raise forms.ValidationError("Email já existe.")

        return new_email


class LoginUserForm(forms.Form):
    username = forms.CharField(label="Nome")
    password = forms.CharField(widget=forms.PasswordInput(), label="Senha")
