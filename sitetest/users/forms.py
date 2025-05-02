import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm, SetPasswordMixin
from django.urls import reverse_lazy


class LoginUserForm(AuthenticationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'password']

    username = forms.CharField()
    password = forms.CharField()

    # username = forms.CharField(label='Логин или E-mail',
    #                            widget=forms.TextInput(attrs={'class': 'form-input'}))

    # password = forms.CharField(label='Пароль',
    #                            widget=forms.PasswordInput(attrs={'class': 'form-input'}))




# class RegisterUserForm(forms.ModelForm):
#     username = forms.CharField(label='Логин')
#     password = forms.CharField(label='Пароль',widget=forms.PasswordInput())
#     password2 = forms.CharField(label='Повтор пароля',widget=forms.PasswordInput())
#
#     class Meta:
#         model = get_user_model()
#         fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password2']
#         labels = {
#             'email': 'E-mail',
#             'first_name': 'Имя',
#             'last_name': 'Фамилия',
#         }
#
#     def clean_password2(self):
#         cd = self.cleaned_data
#         if cd['password'] != cd['password2']:
#             raise forms.ValidationError('Пароли не совпадают')
#         return cd['password']
#
#     def clean_email(self):
#         email = self.cleaned_data['email']
#         if get_user_model().objects.filter(email=email).exists():
#             raise forms.ValidationError('Такой E-mail уже есть в базе данных')
#         return email

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль',widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля',widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        )
    
    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField()
    email = forms.CharField()
    password1 = forms.CharField()
    password2 = forms.CharField()


        # fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        # labels = {
        #     'email': 'E-mail',
        #     'first_name': 'Имя',
        #     'last_name': 'Фамилия',
        # }
        # widgets = {
        #     'email': forms.TextInput(attrs={'class': 'form-input'}),
        #     'first_name': forms.TextInput(attrs={'class': 'form-input'}),
        #     'last_name': forms.TextInput(attrs={'class': 'form-input'}),
        # }

    # def clean_password2(self): # происходит в UserCreationForm
    #     cd = self.cleaned_data
    #     if cd['password1'] != cd['password2']:
    #         raise forms.ValidationError('Пароли не совпадают')
    #     return cd['password1']

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Такой E-mail уже есть в базе данных')
        return email




class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(disabled=True, label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.CharField(disabled=True, label='E-mail', widget=forms.TextInput(attrs={'class': 'form-input'}))
    this_year = datetime.date.today().year
    date_birth = forms.DateTimeField(widget=forms.SelectDateWidget(years=tuple(range(this_year-100, this_year-2))))

    class Meta:
        model = get_user_model()
        fields = ['photo', 'username', 'email', 'first_name', 'last_name', 'date_birth']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
        }




class UserPasswordChangeForm(PasswordChangeForm):

    old_password = forms.CharField(label='Старый пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password1 = forms.CharField(label='Новый пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

