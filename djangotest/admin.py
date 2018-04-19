from django.contrib import admin
from django.forms import ModelForm
from django import forms

from djangotest.models import Customer,Room

# Register your models here.


# class RoomAdminForm(ModelForm):
#     class Meta:
#         model = Room
#         fields = "__all__"
#         widgets = {
#             'image1':forms.ImageInput ,
#         }

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    list_display_links = None
    def has_add_permission(self, request):
        return False

class RoomAdmin(admin.ModelAdmin):
    fields = ('image1_tag',)
    readonly_fields = ('image_tag',)
    list_display = ('type', 'price','image1','image2','image3','image4')


admin.site.register(Customer,CustomerAdmin)
admin.site.register(Room,RoomAdmin)