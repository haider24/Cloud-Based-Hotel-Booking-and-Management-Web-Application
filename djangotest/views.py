from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from djangotest.forms import CustomerForm
from djangotest.models import Customer


def index(request):
    template = loader.get_template('homepage.html')

    return HttpResponse(template.render())
# Create your views here.

def login(request):
    if request.method == "POST":
        userEmail=request.POST.get('email')
        userPassword=request.POST.get('password')
        try:
            user = Customer.objects.get(email=userEmail,password=userPassword)
        except Customer.DoesNotExist:
            user=None
        if user == None:
            template = loader.get_template('failed.html')
            return HttpResponse(template.render())
        else:
            template = loader.get_template('test.html')
            context={}
            context['user']=user
            return HttpResponse(template.render(context,request))


    template=loader.get_template('login.html')
    return HttpResponse(template.render())

def signup(request):
    if request.method == "POST":
        data = CustomerForm(request.POST,request.FILES)
        newCustomer = data.save()
        template = loader.get_template('test.html')
        context={}
        context['form']=data
        return HttpResponse(template.render(context,request))

    template = loader.get_template('signup.html')
    form = CustomerForm()
    context = {}
    context['form'] = form
    return HttpResponse(template.render(context, request))
