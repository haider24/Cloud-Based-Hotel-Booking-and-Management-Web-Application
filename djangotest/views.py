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
    if request.method == "POST":
        data = CustomerForm(request.POST,request.FILES)
        newCustomer = data.save()
        template = loader.get_template('test.html')
        return HttpResponse(template.render())

    template = loader.get_template('signup.html')
    form = CustomerForm()
    context = {}
    context['form'] = form
    return HttpResponse(template.render(context, request))
