from django.contrib import admin
from django.forms import ModelForm
from django import forms

from djangotest.models import Profile,Room,RoomType,Comment,Image

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


admin.site.register(Profile,ProfileAdmin)
admin.site.register(Room,RoomAdmin)
admin.site.register(RoomType)
admin.site.register(Comment,CommentAdmin)
admin.site.register(Image)