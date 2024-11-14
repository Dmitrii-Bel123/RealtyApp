from django import forms
from realty.models import TypeObject, District, Street, Owner, Object, Advert
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class':'form-control'}))

class RegistrationForm(UserCreationForm):
    username = forms.RegexField(label="Имя пользователя:", max_length=30,
        regex=r'^[\w.@+-]+$', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="Email:", max_length=254,
        widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="Пароль:",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Повторите пароль:",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        

class DistrictForm(forms.ModelForm):
    title = forms.CharField(label='Название', widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model = District
        fields = ['title']

class StreetForm(forms.ModelForm):
    title = forms.CharField(label='Название', widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model = Street
        fields = ['title']

class TypeObjectForm(forms.ModelForm):
    title = forms.CharField(label='Название', widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model = TypeObject
        fields = ['title']

class OwnerForm(forms.ModelForm):
    fio = forms.CharField(label='ФИО', widget=forms.TextInput(attrs={'class':'form-control form-control-sm'}))
    phone = forms.CharField(label='Телефон', widget=forms.TextInput(attrs={'class':'form-control form-control-sm'}))
    class Meta:
        model = Owner
        fields = ['fio', 'phone']

class ObjectForm(forms.ModelForm):
    type = forms.ModelChoiceField(label='Тип', queryset=TypeObject.objects.all(), empty_label='', widget=forms.Select(attrs={'class':'form-select form-select-sm'}))
    district = forms.ModelChoiceField(label='Район', queryset=District.objects.all(), empty_label='', widget=forms.Select(attrs={'class':'form-select form-select-sm'}))
    street = forms.ModelChoiceField(label='Улица', queryset=Street.objects.all(), empty_label='', widget=forms.Select(attrs={'class':'form-select form-select-sm'}))
    building = forms.CharField(label='Дом', max_length=10, widget=forms.TextInput(attrs={'class':'form-control form-control-sm'}))
    apartment = forms.CharField(label='Кв.', max_length=10, required=False, widget=forms.TextInput(attrs={'class':'form-control form-control-sm'}))
    apart_area = forms.IntegerField(label='Площадь (кв.м)', required=False, widget=forms.TextInput(attrs={'class':'form-control form-control-sm'}))
    land_area = forms.IntegerField(label='Площадь участка (сот.)', required=False, widget=forms.TextInput(attrs={'class':'form-control form-control-sm'}))
    rooms = forms.IntegerField(label='Количество комнат', required=False, widget=forms.TextInput(attrs={'class':'form-control form-control-sm'}))
    floor = forms.IntegerField(label='Этаж', required=False, widget=forms.TextInput(attrs={'class':'form-control form-control-sm'}))
    floors = forms.IntegerField(label='Этажей в доме', required=False, widget=forms.TextInput(attrs={'class':'form-control form-control-sm'}))
    description = forms.CharField(label='Описание', required=False, widget=forms.Textarea(attrs={'rows':6, 'cols':40, 'class':'form-control form-control-sm'}))
    class Meta:
        model = Object
        fields = '__all__'

class AdvertForm(forms.ModelForm):
    price = forms.FloatField(label='Цена', widget=forms.TextInput(attrs={'class':'form-control form-control-sm'}))
    class Meta:
        model = Advert
        fields = ['price']

CHOICE_ROOMS = (
    (1, '1 комната'),
    (2, '2 комнаты'),
    (3, '3 комнаты'),
    (4, '4 комнаты'),
    (5, '5 комнат и более'),
)

class FilterForm(forms.Form):
    type = forms.ModelChoiceField(label='Тип', required=False, queryset=TypeObject.objects.all(), empty_label='Любой', widget=forms.Select(attrs={'class':'form-select'}))
    district = forms.ModelChoiceField(label='Район', required=False, queryset=District.objects.all(), empty_label='Любой', widget=forms.Select(attrs={'class':'form-select'}))
    apart_area_from = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'placeholder': 'от', 'class':'form-control'}))
    apart_area_to = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'placeholder': 'до', 'class':'form-control'}))
    rooms = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple(), choices=CHOICE_ROOMS)
    floors_from = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'placeholder': 'от', 'class':'form-control'}))
    floors_to = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'placeholder': 'до', 'class':'form-control'}))
    price_from = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'placeholder': 'от', 'class':'form-control'}))
    price_to = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'placeholder': 'до', 'class':'form-control'}))
