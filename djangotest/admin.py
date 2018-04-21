from django.contrib import admin
from django.forms import ModelForm
from django import forms

from djangotest.models import Customer,Room,RoomType

# Register your models here.


# class RoomAdminForm(ModelForm):
#     class Meta:
#         model = Room
#         fields = "__all__"
#         widgets = {
#             'image1':forms.ImageInput ,
#         }

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'email')
    list_display_links = None
    def has_add_permission(self, request):
        return False

class RoomAdmin(admin.ModelAdmin):
    list_display = ('id','type', 'price')



admin.site.register(Customer,CustomerAdmin)
admin.site.register(Room,RoomAdmin)
admin.site.register(RoomType)