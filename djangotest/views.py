from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from djangotest.forms import CustomerForm


def index(request):
    template = loader.get_template('homepage.html')

    return HttpResponse(template.render())
# Create your views here.

def loginpage(request):
    template=loader.get_template('login.html')
    return HttpResponse(template.render())

def signuppage(request):
    template = loader.get_template('signup.html')
    form = CustomerForm()
    context = {}
    context['form'] = form
    return HttpResponse(template.render(context,request))

def createAccount(request):
    data = CustomerForm(request.POST)
    newCustomer=data.save()
    template = loader.get_template('test.html')
    return HttpResponse(template.render())