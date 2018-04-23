from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader, RequestContext
from djangotest.forms import CustomerForm
from djangotest.models import Customer,Comment


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
            request.session['userid']=user.id
            return render(request, 'profile.html', context)

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

def feedback(request):
    if request.method == "POST":
        customerid=request.session['userid']
        customerComment=request.POST.get('comment')
        user=Customer.objects.get(id=customerid)
        comment=Comment(comment=customerComment,customer=user)
        comment.save()
        allComments=getComments()
        context={'comments':allComments,'user':user}
        return render(request, 'feedback.html', context)
    allComments=getComments
    customerid = request.session['userid']
    user=Customer.objects.get(id=customerid)
    context = {'comments': allComments, 'user': user}
    return render(request, 'feedback.html', context)

def getComments():
    comments=Comment.objects.all()
    return comments
