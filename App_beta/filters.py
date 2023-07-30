import django_filters
from .models import *
from django import forms


class ServiceFilter(django_filters.FilterSet):

    class Meta:
        model = Service
        fields = ['category','basic_price']