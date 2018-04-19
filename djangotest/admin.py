from django.contrib import admin

from djangotest.models import Customer

# Register your models here.

class CustomerAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
    # def get_actions(self, request):
    #     actions = super(CustomerAdmin, self).get_actions(request)
    #     del actions['edit_permissions']
    #     del actions['add_permissions']
    #     return actions

admin.site.register(Customer,CustomerAdmin)