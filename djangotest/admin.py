from django.contrib import admin

from djangotest.models import Customer

# Register your models here.

class PersonAdmin(admin.ModelAdmin):
    readonly_fields = ('Customer',)
admin.site.register(Customer)