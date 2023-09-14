from django import forms


class LoginForm(forms.Form):
    email_or_phone = forms.CharField(label='Почта/Телефон', max_length=255)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
