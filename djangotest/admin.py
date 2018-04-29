from django.contrib import admin
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from djangotest.models import Profile,Room,RoomType,Comment,Image,Booking

# Register your models here.


# class RoomAdminForm(ModelForm):
#     class Meta:
#         model = Room
#         fields = "__all__"
#         widgets = {
#             'image1':forms.ImageInput ,
#         }

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name','email')
    list_display_links = None
    def has_add_permission(self, request):
        return False

class RoomAdmin(admin.ModelAdmin):
    list_display = ('id','type', 'price')

class CommentAdmin(admin.ModelAdmin):
    list_display =('comment','customername','customeremail')

class BookingAdmin(admin.ModelAdmin):
    list_display = ('Room','RoomNumber','User','Checkin','Checkout','Bill')
    def has_change_permission(self, request, obj=None):
        return False
    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return True

class UserControlAdmin(UserAdmin):
    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False

#admin.site.register(Profile,ProfileAdmin)
admin.site.register(Room,RoomAdmin)
admin.site.register(RoomType)
admin.site.register(Comment,CommentAdmin)
admin.site.register(Image)
admin.site.register(Booking,BookingAdmin)
admin.site.unregister(User)
admin.site.register(User,UserControlAdmin)

admin.site.site_header = 'Cloud Hotel Adminsitration'
admin.site.site_title = 'Cloud Hotel Administration'