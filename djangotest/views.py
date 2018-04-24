from django.shortcuts import render, redirect
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
            request.session['userid']=user.id
            redirect('profile')

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

def profile(request):
    if request.method=="POST":
        newName=request.POST.get('name')
        newEmail=request.POST.get('email')
        newImage=request.FILES.get('image')
        customerid = request.session['userid']
        user = Customer.objects.get(id=customerid)
        user.name=newName
        user.email=newEmail
        if newImage is not None:
            user.profilePicture = newImage
        user.save()
        redirect('profile')
    else:
        customerid = request.session['userid']
        user = Customer.objects.get(id=customerid)
        form = CustomerForm()
        context = {'user': user, 'form': form}
        return render(request, 'profile.html', context)

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

def rating(request):
    if request.method == "POST":
        customerid=request.session['userid']
        customerRating=request.POST.get('rating')
        user=Customer.objects.get(id=customerid)
        user.rating=customerRating
        user.save()
        return redirect('profile')


