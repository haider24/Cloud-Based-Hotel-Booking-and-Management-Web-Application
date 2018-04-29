from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext
from djangotest.models import Profile,Comment,Room,RoomType,Image,Booking
from django.contrib.auth.models import User
from datetime import datetime, date


def index(request):
    if request.user.is_authenticated:
        return redirect('profile')
    else:
        return render(request, 'homepage.html')
# Create your views here.

def signin(request):
    if request.user.is_authenticated:
        return redirect('profile')
    if request.method == "POST":
        userName=request.POST.get('username')
        userPassword=request.POST.get('password')
        user=authenticate(username=userName,password=userPassword)
        if user == None:
            return render(request,'login.html',{'message':'Invalid Username or Password'})
        else:
            login(request,user)
            request.session['booking']=False
            request.session['userBookings']=getUserBookings(user)
            return HttpResponseRedirect('/profile')
    else:
        return render(request, 'login.html')

def signout(request):
    if not request.user.is_authenticated:
        return redirect('index')
    logout(request)
    return redirect('index')


def signup(request):
    if request.user.is_authenticated:
        return redirect('profile')
    if request.method == "POST":
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        image = request.FILES.get('image')
        try:
            checkUser = User.objects.get(username=username)
        except User.DoesNotExist:
            checkUser=None
        if not checkUser is None:
            return render(request,'signup.html',{'message':'Username Already taken'})

        try:
            checkUser = User.objects.get(email=email)
        except User.DoesNotExist:
            checkUser=None
        if not checkUser is None:
            return render(request,'signup.html',{'message':'An account with this Email already exists'})

        user=User.objects.create_user(first_name=name,username=username,email=email,password=password)
        if image is not None:
            user.profile.profilePicture=image
        user.save()
        login(request,user)
        request.session['booking'] = False
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
        return render(request,'profile.html',{'message':'Profile updated Successfully'})
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
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "POST":
        customerRating=request.POST.get('rating')
        user=request.user
        user.profile.rating=customerRating
        user.save()
        return HttpResponseRedirect('/profile')

def changePassword(request):
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "POST":
        user=request.user
        newPassword=request.POST.get('password')
        user.set_password(newPassword)
        user.save()
        update_session_auth_hash(request, user)
        return render(request, 'profile.html',{'message':'Password changed Successfully'})


def test(request):
    roomid=request.POST.get('roomid')
    checkin = request.POST.get('checkin')
    checkout = request.POST.get('checkout')
    return render(request,'test.html',{'checkin':checkin,'checkout':checkout,'roomid':roomid})
    # if request.method=="POST":
    #     to=request.POST.get('to')
    #     fro = request.POST.get('from')
    #     nfro=fro.replace('-','/')
    #     nto=to.replace('-','/')
    #     date_format = "%Y/%m/%d"
    #     checkout=datetime.strptime(nto,date_format)
    #     checkin = datetime.strptime(nfro,date_format)
    #     delta=checkout-checkin
    #     nd=delta.days
    #     print(nd)

    return render(request,'test.html')

def rooms(request):
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method=="POST":
        typeID=request.POST.get('id')
        checkinDate=request.POST.get('checkin')
        checkoutDate = request.POST.get('checkout')
        room=findAvailableRooms(typeID,checkinDate,checkoutDate)
        if room ==None:
            allRooms = RoomType.objects.all()
            allImages = Image.objects.all()
            context = {'rooms': allRooms, 'images': allImages,'message':'Room not available on selected dates, please try different room or select different dates'}
            return render(request, 'rooms.html', context)
        else:
            allImages = Image.objects.all()
            roomType=RoomType.objects.get(id=typeID)
            days=calculateDays(checkinDate,checkoutDate)
            bill=days*roomType.price
            request.session['booking'] = True
            context={'images':allImages,'checkin':checkinDate,'checkout':checkoutDate,'roomType':roomType,'roomid':room.id,'days':days,'bill':bill}
            return render(request,'confirmbooking.html',context)
    else:
        allRooms = RoomType.objects.all()
        allImages = Image.objects.all()
        context = {'rooms': allRooms, 'images': allImages}
        return render(request, 'rooms.html', context)


def findAvailableRooms(typeID,checkinDate,checkoutDate):
    allRooms=Room.objects.filter(type__id=typeID)
    if not allRooms:
        return None
    for room in allRooms:
        if checkifAvailable(room,checkinDate,checkoutDate)==True:
            return room
    return None

def checkifAvailable(room,checkinDate,checkoutDate):
    roomBookings=Booking.objects.filter(room__id=room.id)
    if not roomBookings:
        return True
    else:
        return checkDates(roomBookings,checkinDate,checkoutDate)

def checkDates(roomBookings,checkinDate,checkoutDate):
    year, month, day = checkinDate.split("-")
    convertedCheckin = date(int(year), int(month), int(day))
    year, month, day = checkoutDate.split("-")
    convertedCheckout = date(int(year), int(month), int(day))
    for booking in roomBookings:
        if convertedCheckin>=booking.checkin and convertedCheckin<=booking.checkout:
            return False
        elif convertedCheckout>=booking.checkin and convertedCheckout<booking.checkout:
            return  False

    return True

def calculateDays(checkin,checkout):
    newCheckin = checkin.replace('-', '/')
    newCheckout = checkout.replace('-', '/')
    date_format = "%Y/%m/%d"
    convertedCheckin = datetime.strptime(newCheckin, date_format)
    convertedCheckout = datetime.strptime(newCheckout, date_format)
    delta = convertedCheckout-convertedCheckin
    return delta.days

def booking(request):
    if not request.user.is_authenticated:
        return redirect('index')
    booinginProgress=request.session['booking']
    if not booinginProgress:
        return redirect('index')
    roomID=request.POST.get('roomid')
    checkinDate=request.POST.get('checkin')
    checkoutDate=request.POST.get('checkout')
    room=Room.objects.get(id=roomID)
    user=request.user
    days=calculateDays(checkinDate,checkoutDate)
    bill=room.type.price*days
    booking=Booking.objects.create(user=user,room=room,checkin=checkinDate,checkout=checkoutDate,bill=bill)
    request.session['booking'] = False
    request.session['userBookings'] = getUserBookings(user)
    return render(request,'test.html')

def cancelBooking(request):
    if not request.user.is_authenticated:
        return redirect('index')
    request.session['booking'] = False
    return redirect('rooms')

def getUserBookings(user):
    bookings=Booking.objects.filter(user__username=user.username)
    return bookings.count()

def myBookings(request):
    if not request.user.is_authenticated:
        return redirect('index')
    user=request.user
    bookings = Booking.objects.filter(user__username=user.username)
    images=Image.objects.all()
    return render(request,'mybookings.html',{'bookings':bookings,'images':images})
