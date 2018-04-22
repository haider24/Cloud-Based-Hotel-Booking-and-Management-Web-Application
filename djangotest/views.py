from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader, RequestContext
from djangotest.forms import CustomerForm
from djangotest.models import Customer


def index(request):
     return render(request,'homepage.html')
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
            return render(request,'failed.html')
        else:
            context={'user':user}
            return render(request, 'test.html', context)

        return render(request,'login.html')


def signup(request):
    if request.method == "POST":
        data = CustomerForm(request.POST,request.FILES)
        newCustomer = data.save()
        context={'form':data}
        return render(request,'test.html',context)

    form = CustomerForm()
    context = {'form':form}
    return render(request,'signup.html',context)
