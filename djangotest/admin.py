from django.contrib import admin
from django.forms import ModelForm
from django import forms

from djangotest.models import Customer,Room

# Register your models here.


class RoomAdminForm(ModelForm):
    class Meta:
        model = Room
        widgets = {
            'image1':forms.ImageField ,
        }

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    list_display_links = None
    def has_add_permission(self, request):
        return False

    class RoomAdmin(admin.ModelAdmin):
        list_display = ('name', 'email')
        form = RoomAdminForm
    # def has_change_permission(self, request, obj=None):
    #     return False


admin.site.register(Customer,CustomerAdmin)
admin.site.register(Room)