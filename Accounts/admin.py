from django.contrib import admin
from .models import Vendor,Address,Customer,Country,Advertisement_Board

# Register your models here.

@admin.register(Advertisement_Board)
class Advertisement_Board_Admin(admin.ModelAdmin):
     list_display=("title","get_image","start_date","end_date","priority","is_active","created_at","updated_at")
@admin.register(Address)
class AddressAdmin (admin.ModelAdmin):
     list_display=("country","city","region","contact","address_line1","unit_number")
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["customer", "customer_image"]

    def customer(self, obj):
        return obj.user.first_name + " " + obj.user.last_name
  
@admin.register(Vendor)
class VendorAdmin (admin.ModelAdmin):
     list_display=["vendor","vendor_image"]
     def vendor(self, obj):
            return obj.user.first_name +" "+obj.user.last_name

     
admin.site.register(Country)



