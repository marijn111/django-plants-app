from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth import authenticate, login, get_user_model, logout
from . import forms
from . import models

import datetime


User = get_user_model()


# Create your views here.
def home_page(request):
    return render(request, 'plants/home_page.html')


def login_page(request):

    if request.POST:
        form = forms.LoginForm(request.POST)
        if form.is_valid():

            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)

                # redirect to succesfull page
                return redirect('/plants')
            else:

                print(form.errors)
            # context['form'] = forms.LoginForm()

    else:
        form = forms.LoginForm()

    context = {'form': form}

    return render(request, 'plants/login_page.html', context)


def register_page(request):

    form = forms.RegisterForm(request.POST or None)
    context = {'form': form}

    if form.is_valid():

        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')

        new_user = User.objects.create_user(username, email, password)

        if new_user is not None:
            return redirect('/')

    return render(request, 'plants/register_page.html', context)


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/')


class PlantListView(LoginRequiredMixin, ListView):
    login_url = '/login'

    template_name = 'plants/plants_overview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return models.Plant.objects.filter(user=self.request.user)


class PlantItemView(LoginRequiredMixin, DetailView):
    login_url = '/login'

    template_name = 'plants/plants_detail.html'
    # , id = self.get_slug_field()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return models.Plant.objects.filter(user=self.request.user, id=self.kwargs.get('pk'))


def delete_plant(request, plant_id):
    models.Plant.objects.get(id=plant_id).delete()

    return redirect('/plants')


@login_required(login_url='/login')
def new_plant(request):

    if request.POST:

        form = forms.AddPlantForm(request.POST, request.FILES)

        if form.is_valid():
            name = form.cleaned_data.get('name')
            description = form.cleaned_data.get('description')
            age = form.cleaned_data.get('age')
            watering = form.cleaned_data.get('watering')
            standplace = form.cleaned_data.get('standplace')
            image = form.cleaned_data.get('image')
            last_watered = form.cleaned_data.get('last_watered')

            water_interval_days = round(31 / watering)

            next_water_day = last_watered + datetime.timedelta(days=water_interval_days)

            user = request.user

            newly_added_plant = models.Plant.objects.create(
                user=user,
                name=name,
                description=description,
                watering=watering,
                standplace=standplace,
                age=age,
                image=image
            )
            newly_added_plant.save()

            next_watering_task = models.Task.objects.create(
                user=user,
                plant=newly_added_plant,
                description="Give {} some water bro".format(name),
                date=next_water_day
            )

            next_watering_task.save()

            if newly_added_plant is not None and next_watering_task is not None:
                return redirect('/plants')

    else:
        form = forms.AddPlantForm()

    context = {'form': form}

    return render(request, 'plants/add_plant.html', context)


@login_required
def tasks(request):

    context = {}

    if request.POST:
        form = forms.TaskDateFilter(request.POST)

        if form.is_valid():
            date = form.cleaned_data.get('date')
            print(date)

    else:
        form = forms.TaskDateFilter()
        date = datetime.datetime.now()

    context['date'] = date
    context['form'] = form

    tasks = models.Task.objects.filter(user=request.user, date=date)

    if tasks.count() < 1:
        context['message'] = "No tasks for the selected date bro.."
    else:
        context['tasks'] = tasks

    return render(request, 'plants/tasks.html', context)
