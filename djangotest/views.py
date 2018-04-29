from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext
from djangotest.models import Profile,Comment,Room,RoomType,Image,Booking
from django.contrib.auth.models import User
from datetime import datetime, date


def index(request):
    if request.user.is_authenticated:     #if user is logged in then redirect to his profile page
        return redirect('profile')
    else:
        return render(request, 'homepage.html')

def signin(request):
    if request.user.is_authenticated:    #if user is logged in then redirect to his profile page
        return redirect('profile')
    if request.method == "POST":         #if signin request then authenticate user
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
    else:              #if get request send login page in response
        return render(request, 'login.html')

def signout(request):
    if not request.user.is_authenticated:
        return redirect('index')
    logout(request)
    return redirect('index')


def signup(request):
    if request.user.is_authenticated:      #if user is logged in then redirect to his profile page
        return redirect('profile')
    if request.method == "POST":           #if post request then create new account
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        image = request.FILES.get('image')
        try:
            checkUser = User.objects.get(username=username)
        except User.DoesNotExist:
            checkUser=None
        if not checkUser is None:         #check if username is already taken
            return render(request,'signup.html',{'message':'Username Already taken'})

        try:
            checkUser = User.objects.get(email=email)
        except User.DoesNotExist:
            checkUser=None
        if not checkUser is None:        #check if an account already exists with given email
            return render(request,'signup.html',{'message':'An account with this Email already exists'})

        user=User.objects.create_user(first_name=name,username=username,email=email,password=password)
        if image is not None:
            user.profile.profilePicture=image
        user.save()                     #create account
        login(request,user)             #start user session
        request.session['booking'] = False
        request.session['userBookings'] = getUserBookings(user)
        return redirect('profile')      #redirect to profile page
        #return HttpResponseRedirect('/profile')
    else:
        return render(request, 'signup.html')     #if get request then send signup page in response

def profile(request):
    if not request.user.is_authenticated:   #if user is not logged in then redirect to homepage
        return redirect('index')
    if request.method=="POST":              #if post request then update user profile
        newName=request.POST.get('name')
        newEmail=request.POST.get('email')
        newImage=request.FILES.get('image')
        user = request.user
        user.email=newEmail
        user.first_name=newName
        if newImage is not None:
            user.profile.profilePicture = newImage
        user.save()
        return render(request,'profile.html',{'message':'Profile updated Successfully'})    #send updated profile page with success message
    else:
        return render(request, 'profile.html')     #if get request then return user profile page in response

def feedback(request):
    if not request.user.is_authenticated:    #if user is not logged in then redirect to homepage
        return redirect('index')
    if request.method == "POST":      #if post request then save comment
        customerComment=request.POST.get('comment')
        user=request.user
        comment=Comment(comment=customerComment,user=user)
        comment.save()
        allComments=getComments()
        context={'comments':allComments}
        return render(request, 'feedback.html', context)
    allComments=getComments           #if get request then send feedback page in response
    user=request.user
    context = {'comments': allComments}
    return render(request, 'feedback.html', context)

def getComments():     #helper function to get all comments
    comments=Comment.objects.all()
    return comments

def rating(request):
    if not request.user.is_authenticated:     #if user is not logged in then redirect to homepage
        return redirect('index')
    if request.method == "POST":              #if post request then save rating
        customerRating=request.POST.get('rating')
        user=request.user
        user.profile.rating=customerRating
        user.save()
        return HttpResponseRedirect('/profile')   #redirect to profile page

def changePassword(request):
    if not request.user.is_authenticated:     #if user is not logged in then redirect to his homepage
        return redirect('index')
    if request.method == "POST":      #if post request then change password
        user=request.user
        newPassword=request.POST.get('password')
        user.set_password(newPassword)
        user.save()
        update_session_auth_hash(request, user)     #update user session with new password
        return render(request, 'profile.html',{'message':'Password changed Successfully'})   #return profile page with success message


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
    if not request.user.is_authenticated:    #if user is not logged in then redirect to his homepage
        return redirect('index')
    if request.method=="POST":          #if post request then check if selected room is available on given dates
        typeID=request.POST.get('id')
        checkinDate=request.POST.get('checkin')
        checkoutDate = request.POST.get('checkout')
        room=findAvailableRooms(typeID,checkinDate,checkoutDate)   #find if room is available on given dates
        if room ==None:             #room not available on given dates
            allRooms = RoomType.objects.all()
            allImages = Image.objects.all()
            context = {'rooms': allRooms, 'images': allImages,'message':'Room not available on selected dates, please try different room or select different dates'}
            return render(request, 'rooms.html', context)   #return rooms not available message
        else:   #room available
            allImages = Image.objects.all()
            roomType=RoomType.objects.get(id=typeID)
            days=calculateDays(checkinDate,checkoutDate)
            bill=days*roomType.price
            request.session['booking'] = True
            context={'images':allImages,'checkin':checkinDate,'checkout':checkoutDate,'roomType':roomType,'roomid':room.id,'days':days,'bill':bill}
            return render(request,'confirmbooking.html',context)    #return confirm booking page with booking details
    else:
        allRooms = RoomType.objects.all()
        allImages = Image.objects.all()
        context = {'rooms': allRooms, 'images': allImages}
        return render(request, 'rooms.html', context)


def findAvailableRooms(typeID,checkinDate,checkoutDate):   #helper function to find available rooms
    allRooms=Room.objects.filter(type__id=typeID)
    if not allRooms:
        return None
    for room in allRooms:
        if checkifAvailable(room,checkinDate,checkoutDate)==True:
            return room
    return None

def checkifAvailable(room,checkinDate,checkoutDate):   #helper function to check of room is available on given dates
    roomBookings=Booking.objects.filter(room__id=room.id)
    if not roomBookings:
        return True
    else:
        return checkDates(roomBookings,checkinDate,checkoutDate)

def checkDates(roomBookings,checkinDate,checkoutDate):   #helper function
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

def calculateDays(checkin,checkout):  #helper function to calulate days between checkin and checkout dates
    newCheckin = checkin.replace('-', '/')
    newCheckout = checkout.replace('-', '/')
    date_format = "%Y/%m/%d"
    convertedCheckin = datetime.strptime(newCheckin, date_format)
    convertedCheckout = datetime.strptime(newCheckout, date_format)
    delta = convertedCheckout-convertedCheckin
    return delta.days

def booking(request):
    if not request.user.is_authenticated:  #if user is not logged in then redirect to homepage
        return redirect('index')
    booinginProgress=request.session['booking']
    if not booinginProgress:     #if booking is not in progress then redirect to profile page
        return redirect('index')
    roomID=request.POST.get('roomid')
    checkinDate=request.POST.get('checkin')
    checkoutDate=request.POST.get('checkout')
    room=Room.objects.get(id=roomID)
    user=request.user
    days=calculateDays(checkinDate,checkoutDate)
    bill=room.type.price*days
    booking=Booking.objects.create(user=user,room=room,checkin=checkinDate,checkout=checkoutDate,bill=bill) #add booking in database
    request.session['booking'] = False
    request.session['userBookings'] = getUserBookings(user)
    bookings = Booking.objects.filter(user__username=user.username)
    images = Image.objects.all()
    return render(request, 'mybookings.html', {'bookings': bookings, 'images': images,'message':'Booking Successful!'}) #send booking successfull response

def cancelBooking(request):
    if not request.user.is_authenticated:   #if user is not logged in then redirect to homepage
        return redirect('index')
    request.session['booking'] = False   #cancel booking
    return redirect('rooms')

def getUserBookings(user): #helper function to find number of user bookings
    bookings=Booking.objects.filter(user__username=user.username)
    return bookings.count()

def myBookings(request):
    if not request.user.is_authenticated:   #if user is not logged in then redirect to homepage
        return redirect('index')
    user=request.user
    bookings = Booking.objects.filter(user__username=user.username)
    images=Image.objects.all()
    return render(request,'mybookings.html',{'bookings':bookings,'images':images}) #return response with all of user bookings
