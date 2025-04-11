from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.template.defaultfilters import title

# from django.utils.deconstruct import deconstructible


from .models import Goods, Category,  Supplier

# @deconstructible
# class RussianValidator:
#     ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНПРСТУФХЦЧЩШЬЫЪЭЮЯабвгдеёжзийклмнпрстуфхцчшщыъьэюя0123456789- "
#     code = 'russian'
#
#     def __init__(self, message=None):
#         self.message = message if message else 'Должны присутствовать только русский символы, дефис и пробел'
#
#     def __call__(self, value, *args, **kwargs):
#         if not(set(value) <= set(self.ALLOWED_CHARS)):
#             raise ValidationError(self.message, code=self.code)
# validators=[
#     RussianValidator(),
# ],


class AddGoods(forms.ModelForm):

    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='Категория не выбрана', label='Категория')
    sup = forms.ModelChoiceField(queryset=Supplier.objects.all(), empty_label='Поставщик не выбран', label='Поставщик')
    author = forms.CharField(disabled=True, label='Внес продукцию пользователь:', widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:
        model = Goods


        # fields = '__all__'
        fields = ['title', 'slug', 'photo', 'content', 'is_stock', 'cat', 'sup', 'author']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5}),

        }
        labels = {'slug':'URL',}

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError('длина превышает 50 символов')
        return title



class UploadFileForm(forms.Form):
    file = forms.ImageField(label='Файл')
