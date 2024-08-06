from django.urls import path
from .views import create_records
from . import views

urlpatterns = [
    path('create_records/', views.create_records, name='create_records'),
    path('', views.home_view, name='home'),
    path('django_sign_up/', views.sign_up_by_django, name='sign_up_by_django'),
]