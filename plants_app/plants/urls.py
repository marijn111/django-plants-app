from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('login', views.login_page, name='login'),
    path('register', views.register_page, name='register'),
    path('logout', views.logout_user, name='logout'),
    path('plants', views.PlantListView.as_view(), name='plant-list')
]