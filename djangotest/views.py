from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext
from djangotest.models import Profile,Comment
from django.contrib.auth.models import User


def index(request):
    if request.user.is_authenticated:
        return redirect('profile')
    else:
        return render(request, 'homepage.html')
# Create your views here.

def signin(request):
    if request.method == "POST":
        userName=request.POST.get('username')
        userPassword=request.POST.get('password')
        user=authenticate(username=userName,password=userPassword)
        if user == None:
            return render(request,'failed.html')
        else:
            login(request,user)
            return HttpResponseRedirect('/profile')
    else:
        return render(request, 'login.html')

def signout(request):
    logout(request)
    return redirect('index')


def signup(request):
    if request.method == "POST":
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        image = request.FILES.get('image')
        user=User.objects.create_user(first_name=name,username=username,email=email,password=password)
        if image is not None:
            user.profile.profilePicture=image
        user.save()
        login(request,user)
        return redirect('profile')
        #return HttpResponseRedirect('/profile')
    else:
        return render(request, 'signup.html')

def profile(request):
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method=="POST":
        newName=request.POST.get('name')
        newEmail=request.POST.get('email')
        newImage=request.FILES.get('image')
        user = request.user
        user.email=newEmail
        user.first_name=newName
        if newImage is not None:
            user.profile.profilePicture = newImage
        user.save()
        return HttpResponseRedirect('/profile')
    else:
        return render(request, 'profile.html')

def feedback(request):
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "POST":
        customerComment=request.POST.get('comment')
        user=request.user
        comment=Comment(comment=customerComment,user=user)
        comment.save()
        allComments=getComments()
        context={'comments':allComments}
        return render(request, 'feedback.html', context)
    allComments=getComments
    user=request.user
    context = {'comments': allComments}
    return render(request, 'feedback.html', context)

def getComments():
    comments=Comment.objects.all()
    return comments

def rating(request):
    if request.method == "POST":
        customerRating=request.POST.get('rating')
        user=request.user
        user.profile.rating=customerRating
        user.save()
        return HttpResponseRedirect('/profile')


