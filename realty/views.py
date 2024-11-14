import requests
import json
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, OwnerForm, ObjectForm, StreetForm, AdvertForm, FilterForm, RegistrationForm
from .models import Street, Owner, Object, Advert
from django.contrib.auth.models import User
from django.db.models import Avg

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')  # Перенаправление на страницу после успешного входа
    else:
        form = LoginForm()

    return render(request, 'realty/login.html', {'form': form})


def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            email = form.cleaned_data.get('email')
            user = User.objects.create_user(username, email, raw_password)
            login(request, user)
            return redirect('/')  # Перенаправляем пользователя на главную страницу после успешной регистрации
    else:
        form = RegistrationForm()
    return render(request, 'realty/registration.html', {'form': form})


@login_required(login_url="/login")
def logout_view(request):
    logout(request)
    return redirect('/')  # Перенаправление на страницу после выхода


# Create your views here.
def index(request):
    return render(request, 'realty/index.html', {})


@login_required(login_url="/login")
def advert(request):
    context = {}
    if request.method == 'POST':
        form_owner = OwnerForm(request.POST, prefix="owner")
        form_object = ObjectForm(request.POST, prefix="object")
        form_advert = AdvertForm(request.POST, prefix="advert")
        if form_owner.is_valid() and form_object.is_valid() and form_advert.is_valid():
            phone = form_owner.cleaned_data['phone']
            owner = Owner.objects.filter(phone=phone).first()
            if owner is None:
                owner = form_owner.save()

            object = form_object.save()

            advert = Advert()
            advert.owner = owner
            advert.object = object
            advert.price = form_advert.cleaned_data['price']
            advert.save()

            return redirect(reverse('advert'))
        else:
            context['form_owner'] = form_owner
            context['form_object'] = form_object
            context['form_advert'] = form_advert
    else:
        form_owner = OwnerForm(prefix="owner")
        form_object = ObjectForm(prefix="object")
        form_advert = AdvertForm(prefix="advert")
        context['form_owner'] = form_owner
        context['form_object'] = form_object
        context['form_advert'] = form_advert

    adverts = Advert.objects.select_related('owner','object').order_by('-create_time')[:5]
    context['adverts'] = adverts

    return render(request, 'realty/advert.html', context)


@login_required(login_url="/login")
def streets(request):
    streets = Street.objects.all().order_by('title')
    return render(request, 'realty/streets.html', {'streets': streets})

@login_required(login_url="/login")
def add_street(request):
    if request.method == 'POST':
        form = StreetForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(reverse('streets'))
    else:
        form = StreetForm()
    return render(request, 'realty/add_street.html', {'form': form})

@login_required(login_url="/login")
def edit_street(request, street_id=None):
    street = Street.objects.get(id=street_id)
    if request.method == 'POST':
        form = StreetForm(request.POST, instance=street)
        if form.is_valid():
            form.save()
        return redirect(reverse('streets'))
    else:
        form = StreetForm(initial={'title': street.title})
    return render(request, 'realty/edit_street.html', {'form': form, 'street_id': street_id})


def filter(request):
    context = {}
    data = {}
    form_filter = FilterForm(request.GET)
    if request.GET.get('submit'):
        if form_filter.is_valid():
            data = form_filter.cleaned_data
            context['after_submit'] = True
        else:
            context['after_submit'] = False

    context['form_filter'] = form_filter

    query = Advert.objects.select_related('owner', 'object').order_by('-create_time')
    if data.get('type'):
        query = query.filter(object__type=data.get('type'))
    if data.get('district'):
        query = query.filter(object__district=data.get('district'))
    if data.get('rooms'):
        query = query.filter(object__rooms__in=data.get('rooms'))
    if data.get('apart_area_from'):
        query = query.filter(object__apart_area__gte=data.get('apart_area_from'))
    if data.get('apart_area_to'):
        query = query.filter(object__apart_area__lte=data.get('apart_area_to'))

    if data.get('floors_from'):
        query = query.filter(object__floor__gte=data.get('floors_from'))
    if data.get('floors_to'):
        query = query.filter(object__floor__lte=data.get('floors_to'))

    if data.get('price_from'):
        query = query.filter(price__gte=data.get('price_from'))
    if data.get('price_to'):
        query = query.filter(price__lte=data.get('price_to'))

    avg_query = query.aggregate(avg_price=Avg('price', default=0))
    context['avg_price'] = avg_query['avg_price']

    context['adverts'] = query[:50]
    return render(request, 'realty/filter.html', context)


def show_advert(request, advert_id=None):
    context = {}

    advert = Advert.objects.select_related('owner','object').get(id=advert_id)

    headers = {
        "charset": "utf-8",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    url = "https://www.cbr-xml-daily.ru/latest.js"
    p = requests.get(url, headers=headers)
    if p.status_code != requests.codes.ok:
        advert.price_usd = 0
    else:
        resp = json.loads(p.content)
        rates = resp['rates']
        advert.price_usd = advert.price * rates['USD']

    context['advert'] = advert
    return render(request, 'realty/show_advert.html', context)
