from django.contrib import admin
from .models import CartOrder , CartOrderItem
from Accounts.models import  Address ,Customer
from Payment_Management_API.models import User_Payment_Method
from .forms import CartOrderForm , CartOrderItemForm
from typing import Any
from django.http.request import HttpRequest
from django.db.models.fields.related import ForeignKey
# Register your models here.
@admin.register(CartOrder)
class cartorderAdmin (admin.ModelAdmin):
     form=CartOrderForm
     list_display=['customer','payment_status','order_date','order_status','invoice_no','total_price']
     list_filter = ['order_date']
     def formfield_for_foreignkey(self, db_field: ForeignKey[Any], request: HttpRequest | None, **kwargs: Any) ->  None:
          if db_field.name=="payment_type" and request.user.is_superuser ==False :
               kwargs["queryset"]=User_Payment_Method.objects.filter(user=request.user)
          elif db_field.name=="shipping_address" and request.user.is_superuser == False:
               Customer_object= Customer.objects.filter(user=request.user)
               Customer_addresses_ids=Customer_object.values_list("addresses",flat=True)
               kwargs["queryset"]=Address.objects.filter(id__in=Customer_addresses_ids)
          return super().formfield_for_foreignkey(db_field, request, **kwargs)
@admin.register(CartOrderItem)
class CartOrderItemAdmin (admin.ModelAdmin):
     form=CartOrderItemForm
     def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if obj:  # If the object exists (i.e., it's being edited)
            readonly_fields += ('item',)
        return readonly_fields
     list_display=['order','product','image','qty','total_price']