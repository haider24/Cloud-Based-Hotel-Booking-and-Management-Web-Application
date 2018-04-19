from django.contrib import admin

from djangotest.models import Customer,Room

# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    list_display_links = None
    def has_add_permission(self, request):
        return False

    # def has_change_permission(self, request, obj=None):
    #     return False


admin.site.register(Customer,CustomerAdmin)
admin.site.register(Room)