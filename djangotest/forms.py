from django.db import models
from django.forms import ModelForm
from djangotest.models import Customer

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'