from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth import authenticate, login, get_user_model, logout
from . import forms
from . import models


User = get_user_model()


# Create your views here.
def home_page(request):
    return render(request, 'plants/home_page.html')


def login_page(request):

    if request.POST:
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)

            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)

                # redirect to succesfull page
                print('logged in yay')
                return redirect('/plants')
            else:

                print('nope')
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
    print(plant_id)
    models.Plant.objects.get(id=plant_id).delete()

    return redirect('/plants')
