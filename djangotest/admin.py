from django.contrib import admin

from djangotest.models import Customer

# Register your models here.

admin.site.register(Customer)

class CustomerAdmin(admin.ModelAdmin):
    def get_actions(self, request):
        actions = super(CustomerAdmin, self).get_actions(request)
        del actions['edit_permissions']
        del actions['add_permissions']
        return actions